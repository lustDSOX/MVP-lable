/** Minimal markdown → HTML for public + staff previews */
export function mdToHtml(src: string): string {
  let s = src || ''
  s = s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  s = s.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" class="max-w-full my-3 border border-[#333]" />')
  s = s.replace(/^### (.*)$/gm, '<h3 class="text-lg font-black uppercase mt-3">$1</h3>')
  s = s.replace(/^## (.*)$/gm, '<h2 class="text-xl font-black uppercase mt-3">$1</h2>')
  s = s.replace(/^# (.*)$/gm, '<h1 class="text-2xl font-black uppercase mt-3">$1</h1>')
  s = s.replace(/^> (.*)$/gm, '<blockquote class="border-l-4 border-[#39FF14] pl-3 text-gray-400 my-2">$1</blockquote>')
  s = s.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/\*(.+?)\*/g, '<em>$1</em>')
  s = s.replace(/`([^`]+)`/g, '<code class="bg-[#111] text-[#39FF14] px-1">$1</code>')
  s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-[#39FF14] underline" target="_blank" rel="noopener">$1</a>')
  s = s.replace(/^- (.*)$/gm, '<li>$1</li>')
  s = s.replace(/(<li>.*<\/li>\n?)+/g, (m) => `<ul class="list-disc pl-5 my-2">${m}</ul>`)
  s = s.replace(/\n\n/g, '</p><p class="my-2">')
  return `<p class="my-2">${s}</p>`
}
