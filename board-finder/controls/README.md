# The two control runs

`PREREG_CONTROLS.md` — predictions, committed before either respondent saw anything.
`response_positive.md`, `response_negative.md` — the verbatim respondent texts.
`verdicts.json` — the reading of each response, **field by field, each with the quote
that supports it**.
`score_controls.py` — scores the predictions and fails if any verdict's quote is not
found verbatim in the response it claims to come from.

That last check is the only real defence against scoring my own instrument charitably:
a verdict I cannot quote does not count.
