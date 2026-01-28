import fs from 'node:fs';
import path from 'node:path';

export interface Publication {
  key: string;
  type: string;
  title: string;
  authors: string;
  year: number;
  doi?: string;
  url?: string;
  journal?: string;
  booktitle?: string;
  volume?: string;
  number?: string;
  pages?: string;
  publisher?: string;
}

export function getPublications(): Publication[] {
  const bibPath = path.join(process.cwd(), 'src/data/publications.bib');
  const bibContent = fs.readFileSync(bibPath, 'utf-8');

  const entries = parseBibtex(bibContent);

  return entries
    .filter(entry => entry.keywords?.includes('selected'))
    .map(entry => ({
      key: entry.key,
      type: entry.type,
      title: cleanLatex(entry.title || ''),
      authors: formatAuthors(entry.author || ''),
      year: parseInt(entry.year || '0'),
      doi: cleanDoi(entry.doi),
      url: entry.url,
      journal: cleanLatex(entry.journal || ''),
      booktitle: cleanLatex(entry.booktitle || ''),
      volume: entry.volume,
      number: entry.number,
      pages: entry.pages?.replace('--', '–'),
      publisher: entry.publisher,
    }))
    .sort((a, b) => b.year - a.year);
}

interface BibEntry {
  type: string;
  key: string;
  [field: string]: string | undefined;
}

function parseBibtex(content: string): BibEntry[] {
  const entries: BibEntry[] = [];

  // Match each @type{key, ... } block
  const entryRegex = /@(\w+)\s*\{\s*([^,]+),([^@]*?)(?=\n@|\n*$)/gs;

  let match;
  while ((match = entryRegex.exec(content)) !== null) {
    const type = match[1].toLowerCase();
    const key = match[2].trim();
    const fieldsStr = match[3];

    const entry: BibEntry = { type, key };

    // Parse fields: fieldname = {value} or fieldname = "value" or fieldname = value
    const fieldRegex = /(\w+)\s*=\s*(?:\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}|"([^"]*)"|(\d+))/g;

    let fieldMatch;
    while ((fieldMatch = fieldRegex.exec(fieldsStr)) !== null) {
      const fieldName = fieldMatch[1].toLowerCase();
      const value = fieldMatch[2] || fieldMatch[3] || fieldMatch[4] || '';
      entry[fieldName] = value.trim();
    }

    entries.push(entry);
  }

  return entries;
}

function cleanLatex(text: string): string {
  if (!text) return '';
  return text
    .replace(/\{([^{}]*)\}/g, '$1') // Remove braces but keep content
    .replace(/\\&/g, '&')
    .replace(/\\"/g, '"')
    .replace(/\\\\/g, '')
    .replace(/~/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function cleanDoi(doi?: string): string | undefined {
  if (!doi) return undefined;
  return doi.replace(/^https?:\/\/doi\.org\//, '');
}

function formatAuthors(authorString: string): string {
  if (!authorString) return '';

  return authorString
    .split(' and ')
    .map(author => {
      author = author.trim();
      // Handle "Last, First" format
      if (author.includes(',')) {
        const [last, first] = author.split(',').map(s => s.trim());
        return `${first} ${last}`;
      }
      return author;
    })
    .join(', ');
}
