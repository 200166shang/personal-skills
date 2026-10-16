# Note structure and HTML presentation review

Authors run this checklist after rendering; independent reviewers repeat it against the frozen candidate. Review the actual delivered Markdown and HTML, including the ending. Record concrete observations and locations, not only “looks good”. Content and image review remain required separately.

## Structure and Markdown/HTML correspondence

- Identify the source's topic transitions. Give substantial sections descriptive subheadings grounded in the existing speech, preserving its order and voice. A multi-topic lesson rendered as uninterrupted body text requires a fix. A short, single-topic lesson may omit subheadings; record why. A document title alone is not section structure.
- Check natural paragraph breaks and readable paragraph lengths without fragmenting sentences or converting the lecture into a new outline. Heading levels must express the actual hierarchy.
- Compare the complete final Markdown with the HTML in order: headings and levels, paragraphs, lists, code blocks, figures and captions. Check counts and content, including the final paragraph; hashes alone cannot detect rendering omissions. Verify escaping, code indentation/newlines and special characters. Copy representative commands/code and compare with the Markdown.
- Check that figures sit beside the passage they illustrate, with the correct caption and original source timestamp/part. Assess useful detail at the displayed size and when enlarged; report source-resolution limits.
- For long lessons, verify that the heading-based table of contents exposes the sections and that its anchors resolve to the intended headings. Check source-time link targets against the original part and timestamp.

## Actual page inspection

Open the delivered HTML using an allowed browser surface. Inspect desktop and narrow layouts, covering the beginning, middle, ending and every distinct complex element present (long code, lists, figures and long headings). Check readable text/contrast, wrapping, horizontal overflow and obscured content. Intentional scrolling inside code blocks is acceptable. Test table-of-contents navigation and image zoom, including closing zoom. Verify local images and styles load offline; external source links still require network access. Mark absent element types as not applicable.

If browser access, offline testing or an interaction is unavailable, state the specific untested check and reason in limitations. File/source inspection can establish correspondence but cannot establish viewport appearance or working interactions. Preserve browser access restrictions.

## Findings and evidence

Missing topic subheadings, omitted HTML content, broken anchors/assets, incorrect code rendering or an observed unusable layout are actionable findings requiring FIX in an independent review. Locate each finding by heading/paragraph, image path or HTML element and describe the expected correction. Fix observed defects even when other browser checks are unavailable.

Record content/image review separately from presentation checks. In a batch review result, add a `presentation_review` object containing `structure`, `markdown_html`, and `browser` observations, plus a top-level `limitations` list naming untested checks. For example, `browser` may state the inspected viewport widths and interactions or “not tested; see limitations”. These are caller evidence fields preserved by the batch recorder, not a new automatically enforced schema or proof. In a single-lesson delivery, include the same observations and limitations in the delivery report.

PASS requires no unresolved observed defect and completed content/image and structure/correspondence review. Missing browser capability alone may accompany PASS with explicit limitations; it does not certify page usability. Incomplete source/image review or inability to judge structure/correspondence requires UNCERTAIN. Recheck changed content and rerender/revalidate after author repairs; independent reviewers preserve the candidate and request repairs.
