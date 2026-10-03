export interface Track {
  slug: string;
  title: string;
  file: string;
  duration: string;
  year: number;
  cover: string;
  tags: string[];
  description: string;
}

// Локальные файлы в public/audio/ — нет CORS-проблем
export const release_base = '';

export const tracks: Track[] = [
  {
    slug: 'komfortnyj-ad',
    title: 'Комфортный ад',
    file: 'komfortnyj-ad.mp3',
    duration: '4:20',
    year: 2026,
    cover: '/covers/komfortnyj-ad.jpg',
    tags: ['phonk', 'hyperpop', 'anti-consumerism'],
    description: 'Пробуждение от сна системы. Манифест тех, кто устал быть расходным материалом.',
  },
  {
    slug: 'upgrade-pustoty',
    title: 'Апгрейд пустоты',
    file: 'upgrade-pustoty.mp3',
    duration: '4:55',
    year: 2026,
    cover: '/covers/upgrade-pustoty.png',
    tags: ['phonk', 'industrial', 'transformation'],
    description: 'После взрыва не строю стены. Взрыв — это диагноз. О сборке себя из пепла.',
  },
  {
    slug: 'paketik-dlya-spyashchih',
    title: 'Пакетик для спящих',
    file: 'paketik-dlya-spyashchih.mp3',
    duration: '3:48',
    year: 2026,
    cover: '/covers/paketik-dlya-spyashchih.jpg',
    tags: ['phonk', 'satire', 'awakening'],
    description: 'О тех, кто заваривает собственный сон. Одуванчик против пакетика.',
  },
  {
    slug: 'na-u-yu',
    title: 'На-у-ю',
    file: 'na-u-yu.mp3',
    duration: '3:15',
    year: 2026,
    cover: '/covers/na-u-yu.jpg',
    tags: ['phonk', 'banks', 'freedom'],
    description: 'Все банки в ряд намотаю. Прощание с долговой системой.',
  },
  {
    slug: 'na-u-yu-wrapped',
    title: 'Na-U-Yu Wrapped',
    file: 'na-u-yu-wrapped.mp3',
    duration: '3:15',
    year: 2026,
    cover: '/covers/na-u-yu-wrapped.jpg',
    tags: ['phonk', 'banks', 'english'],
    description: 'English version. All the banks in a row I\'ll wrap.',
  },
];

export default { release_base, tracks };
