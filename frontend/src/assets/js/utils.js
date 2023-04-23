// source : https://stackoverflow.com/questions/4602141/variable-name-as-a-string-in-javascript
// usage : varToString({variableName})
export const varToString = varObj => Object.keys(varObj)[0];

export function sessionGetAndRemove(key, isJsonArray = false) {
  let value = sessionStorage.getItem(key);
  sessionStorage.removeItem(key);

  if (isJsonArray) {
    value = JSON.parse(value);
    if (value == null) {
      value = [];
    }
  }

  return value;
}

export default function () {}
