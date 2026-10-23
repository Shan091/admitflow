// Execute the diagnostic collection locally without exporting credentials or raw responses.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const root = path.resolve(__dirname, '../..');
const runnerPath = process.argv[2];
if (!runnerPath) {
  console.error('Provide the installed Newman module path. Add --send-once for one test send.');
  process.exit(1);
}
const newman = require(path.resolve(runnerPath));
const config = {};
for (const line of fs.readFileSync(path.join(root, 'backend/.env'), 'utf8').split(/\r?\n/)) {
  const match = line.match(/^([A-Za-z_][A-Za-z0-9_]*)=(.*)$/);
  if (!match) continue;
  let value = match[2].trim();
  if ((value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))) value = value.slice(1, -1);
  config[match[1]] = value;
}
const keys = ['WHATSAPP_ACCESS_TOKEN', 'WHATSAPP_PHONE_NUMBER_ID', 'WHATSAPP_TEST_RECIPIENT'];
if (keys.some(key => !config[key])) {
  console.error('Required local WhatsApp configuration is missing.');
  process.exit(1);
}
const collection = JSON.parse(fs.readFileSync(
  path.join(root, 'docs/event/whatsapp-diagnostic.postman_collection.json'), 'utf8'));

function runItem(index) {
  return new Promise((resolve, reject) => {
    const selected = { ...collection, item: [collection.item[index]] };
    const run = newman.run({
      collection: selected,
      envVar: keys.map(key => ({ key, value: config[key], type: 'secret' })),
      reporters: [],
      silent: true,
      iterationCount: 1,
      timeoutRequest: 20000,
    }, (error, summary) => {
      if (error) return reject(new Error('Postman collection execution failed.'));
      console.log(JSON.stringify({
        stage: index === 0 ? 'health' : 'send',
        requests: summary.run.stats.requests.total,
        assertions: summary.run.stats.assertions.total,
        failed_assertions: summary.run.stats.assertions.failed,
        runtime_failures: summary.run.failures.map(failure => ({
          name: failure.error.name,
          message: keys.reduce((message, key) => message.split(config[key]).join('[redacted]'),
            String(failure.error.message)),
        })),
      }));
      resolve();
    });
    run.on('request', (error, args) => {
      const result = { stage: index === 0 ? 'health' : 'send' };
      if (error) {
        result.transport_error = true;
      } else {
        result.http_status = args.response.code;
        try {
          const data = args.response.json();
          if (index === 0) {
            result.sending = data.health_status?.can_send_message;
            result.entities = (data.health_status?.entities || []).map(entity => ({
              type: entity.entity_type,
              sending: entity.can_send_message,
              error_codes: (entity.errors || []).map(issue => issue.error_code),
            }));
          } else {
            result.accepted = Boolean(data.messages?.[0]?.id);
            if (data.messages?.[0]?.id) {
              result.message_ref = crypto.createHash('sha256')
                .update(data.messages[0].id).digest('hex').slice(0, 12);
            }
          }
          if (data.error) result.api_error_code = data.error.code;
        } catch {
          result.response_not_json = true;
        }
      }
      console.log(JSON.stringify(result));
    });
  });
}

(async () => {
  await runItem(0);
  // Explicit user-authorized final retry, even if health reports a block.
  // Default execution performs only the read-only health check.
  if (process.argv.includes('--send-once')) await runItem(1);
})().catch(() => {
  console.error('Diagnostic failed. Raw errors suppressed to protect credentials.');
  process.exitCode = 1;
});
