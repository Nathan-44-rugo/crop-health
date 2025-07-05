export function stripMarkdown(md: string): string {
  return md
    // Remove bold **text** and __text__
    .replace(/\*\*(.+?)\*\*/g, '$1')
    .replace(/__(.+?)__/g, '$1')
    // Remove italic *text* or _text_
    .replace(/\*(.+?)\*/g, '$1')
    .replace(/_(.+?)_/g, '$1')
    // Remove headings ###
    .replace(/^#{1,6}\s*/gm, '')
    // Remove list markers -, *, + or numbered lists
    .replace(/^\s*[\-\*\+]\s+/gm, '')
    .replace(/^\s*\d+\.\s+/gm, '')
    // Remove blockquote >
    .replace(/^\s*>\s+/gm, '')
    // Remove inline code `text`
    .replace(/`(.+?)`/g, '$1')
    // Remove code fences ```...```
    .replace(/```[\s\S]*?```/g, '')
    // Collapse multiple newlines into 2
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}
