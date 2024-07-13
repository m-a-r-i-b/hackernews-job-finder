import { TECHNOLOGY_COLORS } from './Constants';


export function assignColorToKeyword(keyword) {
  let languageColor = null;
  let longestKey = '';

  // Loop through all the keys in TECHNOLOGY_COLORS
  for (const key in TECHNOLOGY_COLORS) {
    if (keyword.toLowerCase() == key && key.length > longestKey.length) {
      longestKey = key;
      languageColor = TECHNOLOGY_COLORS[key];
    }
  }

  return languageColor;
}

