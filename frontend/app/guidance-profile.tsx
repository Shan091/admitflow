export type GuidanceProfile = {
  stage: "exploring" | "comparing" | "decided";
  deeper: boolean;
  notes: { topic: string; evidence: string }[];
  themes: { theme: string; evidence: string }[];
};

const stages = {
  exploring: "Exploring options",
  comparing: "Comparing options",
  decided: "Has a course in mind",
};
const topics: Record<string, string> = {
  background: "Education and experience",
  interest: "Interests",
  strength: "Self-reported strengths",
  value: "What matters to the student",
  constraint: "Practical considerations",
  goal: "Goals",
  avoid: "Things they prefer to avoid",
  decision: "Course preference",
};

export default function StudentGuidance({ profile }: { profile?: GuidanceProfile }) {
  if (!profile) return null;
  return (
    <section className="guidance-profile" aria-label="Course guidance">
      <h3>Course guidance</h3>
      <p>
        <strong>{stages[profile.stage] || "Exploring options"}</strong>
        {profile.deeper ? " · Deeper exploration requested" : ""}
      </p>
      <p className="quiet small">
        Student-stated preferences and tentative interest themes. These are
        guidance notes, not an aptitude test or an eligibility decision.
      </p>
      {profile.notes.length ? (
        <dl className="guidance-notes">
          {Object.entries(topics).map(([topic, label]) => {
            const notes = profile.notes.filter((note) => note.topic === topic);
            if (!notes.length) return null;
            return (
              <div key={topic}>
                <dt>{label}</dt>
                <dd>
                  {notes.map((note, index) => (
                    <p key={`${topic}-${index}`}>{note.evidence}</p>
                  ))}
                </dd>
              </div>
            );
          })}
        </dl>
      ) : (
        <p className="quiet">No interests or background have been recorded yet.</p>
      )}
      {profile.themes.length > 0 && (
        <details className="evidence">
          <summary>View tentative interest themes</summary>
          {profile.themes.map((theme, index) => (
            <p key={`${theme.theme}-${index}`}>
              <strong>{theme.theme}</strong>: {theme.evidence}
            </p>
          ))}
        </details>
      )}
    </section>
  );
}
