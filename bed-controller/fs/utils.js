// --- Helper for Pure JavaScript Number-to-String Conversion ---
// This function solves the MJS bug where ('' + number) or toString() fails.
// It supports formatting to a fixed number of decimal places.
// v1.1: Added decimal support
// v1.2: Fixed Math.pow() by using multiplication
// v1.3: Removed String() fallback (which caused crashes when chr was undefined)

function numToStrJS(num, decimals) {
    // Default decimals to 0 if not provided or invalid
    if (typeof decimals === 'undefined' || decimals < 0) {
        decimals = 0;
    }

    // Handle zero case
    if (num === 0) {
        if (decimals === 2) return "0.00";
        return "0";
    }

    // chr() is a global MJS function that converts ASCII code to character.
    // It *must* be available (e.g., by loading 'api_mjs.js' in init.js)
    if (typeof chr === 'undefined') {
        print('!!! FATAL ERROR in numToStrJS: chr() is not defined!');
        return "ERR"; // Return an error string
    }

    let is_negative = false;
    if (num < 0) {
        is_negative = true;
        num = -num;
    }

    // Handle decimal part
    let intPart = Math.floor(num);
    let fracPart = num - intPart;
    let fracStr = "";

    if (decimals === 2) {
        // Calculate the 2 decimal digits by multiplying by 100 and rounding
        let fracVal = Math.round(fracPart * 100); // e.g., 0.456 -> 45.6 -> 46. 0.051 -> 5.1 -> 5

        // Convert the 2-digit fractional part to a string
        if (fracVal === 0) {
            fracStr = "00";
        } else if (fracVal < 10) {
            fracStr = "0" + chr(fracVal + 48); // e.g., 0.05 -> fracVal=5 -> "05"
        } else if (fracVal >= 100) { 
            // Handle rounding up from 0.995+
            fracVal = 0; // The integer part will be incremented
            intPart += 1;
            fracStr = "00";
        } else {
            // Standard case, e.g., 45
            let digit1 = fracVal % 10;
            let digit2 = Math.floor(fracVal / 10);
            fracStr = chr(digit2 + 48) + chr(digit1 + 48); // e.g., 0.45 -> fracVal=45 -> "4" + "5"
        }
    }

    // Convert integer part
    let intStr = "";
    if (intPart === 0) {
        intStr = "0";
    } else {
        let tempInt = intPart;
        while (tempInt > 0) {
            let digit = tempInt % 10;
            intStr = chr(digit + 48) + intStr;
            tempInt = Math.floor(tempInt / 10);
        }
    }

    let result = intStr;
    if (decimals === 2) {
        result += "." + fracStr;
    }

    if (is_negative) {
        result = chr(45) + result; // Add ASCII for '-'
    }

    return result;
}


