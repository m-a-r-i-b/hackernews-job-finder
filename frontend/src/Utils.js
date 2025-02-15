import { TECHNOLOGY_COLORS } from './Constants';


export function assignColorToKeyword(keyword) {
  let languageColor = null;
  let longestKey = '';

  // Loop through all the keys in TECHNOLOGY_COLORS
  for (const key in TECHNOLOGY_COLORS) {
    if (keyword.toLowerCase() === key && key.length > longestKey.length) {
      longestKey = key;
      languageColor = TECHNOLOGY_COLORS[key];
    }
  }

  return languageColor;
}



export function parseComment(msgObj){

  if (msgObj){
      if (msgObj.IS_REMOTE_WORK_ALLOWED){
        // Check if If msgObj.IS_REMOTE_WORK_ALLOWED is of type object, 
        // extract allows_remote_work key and assign it to IS_REMOTE_WORK_ALLOWED
        // Otherwise dont change anything
        if (typeof msgObj.IS_REMOTE_WORK_ALLOWED === 'object'){

          if (msgObj.IS_REMOTE_WORK_ALLOWED.allows_remote_work === false){
            // Mark other columns as N/A
            msgObj.EXTRACT_ROLES = '-'
            msgObj.EXTRACT_KEYWORDS = '-'
            msgObj.EXTRACT_CONTACT_INFO = '-'
            msgObj.GENERATE_COVER_LETTER = '-'

          }

          msgObj.IS_REMOTE_WORK_ALLOWED = String(msgObj.IS_REMOTE_WORK_ALLOWED.allows_remote_work)
        }
      }

      if (msgObj.EXTRACT_KEYWORDS){
        if (typeof msgObj.EXTRACT_KEYWORDS === 'object'){
          if (msgObj.EXTRACT_KEYWORDS.keywords.length === 0){
            msgObj.EXTRACT_KEYWORDS = '-'
          } else{
            msgObj.EXTRACT_KEYWORDS = msgObj.EXTRACT_KEYWORDS.keywords.join(', ')
          }
        }
      }

      if (msgObj.EXTRACT_ROLES){
        if (typeof msgObj.EXTRACT_ROLES === 'object'){
          if (msgObj.EXTRACT_ROLES.roles.length === 0){
            msgObj.EXTRACT_ROLES = '-'
          } else{
            msgObj.EXTRACT_ROLES = msgObj.EXTRACT_ROLES.roles.join(', ')
          }
        }
      }

      if (msgObj.EXTRACT_CONTACT_INFO){
        if (typeof msgObj.EXTRACT_CONTACT_INFO === 'object'){
          msgObj.EXTRACT_CONTACT_INFO = msgObj.EXTRACT_CONTACT_INFO.contact_info.join(', ')
        }
      }

      if (msgObj.GENERATE_COVER_LETTER){
        if (typeof msgObj.GENERATE_COVER_LETTER === 'object'){
          msgObj.GENERATE_COVER_LETTER = msgObj.GENERATE_COVER_LETTER.cover_letter
        }
      }
  }

  return msgObj
}