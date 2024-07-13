export function parseComment(msgObj){

    if (msgObj){
        if (msgObj.IS_REMOTE_WORK_ALLOWED){
          // Check if If msgObj.IS_REMOTE_WORK_ALLOWED is of type object, 
          // extract allows_remote_work key and assign it to IS_REMOTE_WORK_ALLOWED
          // Otherwise dont change anything
          if (typeof msgObj.IS_REMOTE_WORK_ALLOWED === 'object'){
            msgObj.IS_REMOTE_WORK_ALLOWED = String(msgObj.IS_REMOTE_WORK_ALLOWED.allows_remote_work)
          }
        }

        if (msgObj.EXTRACT_KEYWORDS){
          if (typeof msgObj.EXTRACT_KEYWORDS === 'object'){
            msgObj.EXTRACT_KEYWORDS = msgObj.EXTRACT_KEYWORDS.keywords.join(', ')
          }
        }

        if (msgObj.EXTRACT_ROLES){
          if (typeof msgObj.EXTRACT_ROLES === 'object'){
            msgObj.EXTRACT_ROLES = msgObj.EXTRACT_ROLES.roles.join(', ')
          }
        }

        if (msgObj.EXTRACT_CONTRACT_INFO){
          if (typeof msgObj.EXTRACT_CONTRACT_INFO === 'object'){
            msgObj.EXTRACT_CONTRACT_INFO = msgObj.EXTRACT_CONTRACT_INFO.contact_info.join(', ')
          }
        }
    }

    return msgObj
}