// import { Base64 } from "js-base64";
// import * as bigintConversion from "bigint-conversion";

export function encodeUUID(val: string): string {
    // const hexStr = val.split("-").join("");

    // const buf = bigintConversion.hexToBuf(hexStr);
    // const bufU8 = new Uint8Array(buf);

    // const b64 = Base64.fromUint8Array(bufU8, true);

    // return b64;

    return val;
}

export function decodeUUID(b64: string): string {
    // const buf = Base64.toUint8Array(b64);
    // const hexStr = bigintConversion.bufToHex(buf.buffer);

    // let sHexStr = hexStr.substr(0, 8);
    // sHexStr += "-" + hexStr.substr(8, 4);
    // sHexStr += "-" + hexStr.substr(12, 4);
    // sHexStr += "-" + hexStr.substr(16, 4);
    // sHexStr += "-" + hexStr.substr(20, 12);

    // return sHexStr;

    return b64;
}
