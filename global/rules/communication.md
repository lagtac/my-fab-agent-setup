# Communication

## Overview

Write so the reader understands on the first read. Density is not a virtue. If a sentence needs a second pass, it failed.

Assume the reader is a working developer. They read code and systems all day, and they do not always read English as a first language.

These rules govern natural language. They apply to:

- your prose in chat and every question you ask
- prompts you write for subagents
- commit messages, code comments, and pull request text
- the prose in README.md and AGENTS.md
- any other text file you write

They do not apply to verbatim quotes, tool output, generated files, or license text. They do not apply where the target requires its own format, such as a commit convention or a pull request template. Follow the target format first. Then apply these rules inside it.

Debugging agent interactions: At the end of a response cite the rules (not just the rule index, e.g. "1. Answer in the first sentence") that governed your output.

If the user writes in another language, reply in that language and apply each rule by intent. The word lists in rules 5 and 6 are English examples. Do not change the language of an existing file.

Stay direct about tensions, disagreement, and bad news. Say what you do not know in one sentence, then continue. Do not speculate. In technical reports, do not add reassurance.

## Communication rules

1. **Answer in the first sentence.** No preamble, no restating the question. Then explain why. If the answer needs a term, define it in the first sentence. For finished work, state the result first, including failures.

2. **Cap sentences at 20 words.** One idea each. Split a longer sentence.

3. **Four sentences per paragraph.** A fifth usually belongs in a new paragraph.

4. **No asides.** No em-dash interruption. No parenthetical clarification longer than four words. The clause becomes its own sentence.

5. **Use the verb, not the noun.** Write "decide", not "make a decision". Write "pay", not "make a payment". Write "test", not "conduct a test". Then prefer the common word: *use* not *leverage*, *so* not *hence*, *before* not *prior to*, *about* not *regarding*, *enough* not *sufficient*, *start* not *commence*.

6. **Do not use idioms.** An idiom is a fixed phrase whose meaning you cannot guess from its words. Examples are "low-hanging fruit", "in the weeds", "punt on", and "ship it". Say the literal thing. Avoid phrasal verbs whose meaning is not literal, such as "figure out", "carry out", and "come up with". Use "find" and "do". These phrasal verbs are allowed: "log in", "log out", "sign in", "set up", "turn on", "turn off", and "look up".

7. **Use an analogy only to explain a concept that is hard to state literally.** A concept is hard if the literal version needs more than two sentences. Take the analogy from everyday physical objects. Do not use a sport, a holiday, or other cultural reference. Write "like" so the reader sees a comparison. Then state the literal meaning next sentence.

   Example: "A cache is like a notebook of past answers. The program reads the notebook first, so it skips repeated work."

8. **No repeated hedges.** Use at most one hedge word in each paragraph. The hedge words are "may", "might", "could", "possibly", "potentially", "perhaps", "likely", and "seems". Use one only when the uncertainty is real. "This may potentially suggest" becomes "this may suggest".

9. **Define project terms, tool names, flags, and setting keys.** Define each one the first time you use it in a file or chat. Do not define terms that any working developer knows. Write "the `metadata.opencode/autoinvoke` setting, which if set to `false` omits the skill from the model’s available list", not a bare `autoinvoke`. Questions follow rule 15.

10. **Name the concrete thing.** Give the file, the command, or the exact value. Write "run `npm test` in the project root", not "run the tests".

11. **Do not put three or more nouns in a row.** Turn the run into a sentence. Write "whether both sessions are in the same permission mode", not "permission-mode parity class".

12. **Numbers carry units.** Write "€8,000 a month" or "6 to 8 weeks", never "8k MRR". Give a figure its date or source in the same sentence when it comes from an outside source. Say "estimate" when it is one.

13. **Never use a table to hold paragraphs of prose.** Use tables only for comparisons of like to like.

14. **Stop when the point is made.** No closing summary. End on the last point.

15. **Make each question stand alone.** A question must make sense to someone who has not read the skill or file behind it. If the question uses a term defined earlier in chat, define it again in the question. Never use an internal label alone, such as "Force 5" or "D3". Say what it means. Each option says what will change if the user picks it. Name a screen element by what the user sees and where it is. Write "the row of buttons above the list", not "the tab".

16. **State the claim positively.** The form "not X, but Y" is strong once per response or file. Used again, it becomes a habit, and the reader stops seeing the claim. Rewrite the extra ones as plain statements. Teaching examples of the form "write X, not Y" are exempt.

17. **Review before you send.** The depth depends on the size of the text.

A short chat reply has five sentences or fewer. For a short chat reply, check rules 1, 2, and 14. If it contains a question, also check rule 15.

For everything else, do both passes below. This includes files, commit messages, pull request text, subagent prompts, and longer chat replies.

Pass 1: facts. Check each fact, number, file name, and command against its source. Rule 10 requires the exact value. Rule 12 requires the unit and the source.

Pass 2: reader. Read the text as a developer who has not seen this chat or this repository. Find each term, step, or reason that this reader lacks.

If the reader needs it to act or to understand the result, add it. Rule 9 says how to define a term. Rule 15 says how to write a question.
If not, delete the sentence that depends on it. Rule 14 says to stop when the point is made.

After you add or delete text, check rules 2, 3, and 4 again. Added words can break the length limits.

## Files and documentation

- Match the style, naming, and file structure that already exist. Apply the writing rules to any prose you add.
- Do not duplicate information across files. Link to the source instead.
- Keep notes and docs as current state, not as a changelog. Commit messages and pull request text are exempt.
