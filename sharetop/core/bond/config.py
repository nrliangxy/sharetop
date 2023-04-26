from pathlib import Path

HERE = Path(__file__).parent

# 债券基本信息表头
EASTMONEY_BOND_BASE_INFO_FIELDS = {
    'SECURITY_CODE': '债券代码',
    'SECURITY_NAME_ABBR': '债券名称',
    'CONVERT_STOCK_CODE': '正股代码',
    'SECURITY_SHORT_NAME': '正股名称',
    'RATING': '债券评级',
    'PUBLIC_START_DATE': '申购日期',
    'ACTUAL_ISSUE_SCALE': '发行规模(亿)',
    'ONLINE_GENERAL_LWR': '网上发行中签率(%)',
    'LISTING_DATE': '上市日期',
    'EXPIRE_DATE': '到期日期',
    'BOND_EXPIRE': '期限(年)',
    'INTEREST_RATE_EXPLAIN': '利率说明',
}

js_str = """
    function mcode(input) {  
                var keyStr = "ABCDEFGHIJKLMNOP" + "QRSTUVWXYZabcdef" + "ghijklmnopqrstuv"   + "wxyz0123456789+/" + "=";  
                var output = "";  
                var chr1, chr2, chr3 = "";  
                var enc1, enc2, enc3, enc4 = "";  
                var i = 0;  
                do {  
                    chr1 = input.charCodeAt(i++);  
                    chr2 = input.charCodeAt(i++);  
                    chr3 = input.charCodeAt(i++);  
                    enc1 = chr1 >> 2;  
                    enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);  
                    enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);  
                    enc4 = chr3 & 63;  
                    if (isNaN(chr2)) {  
                        enc3 = enc4 = 64;  
                    } else if (isNaN(chr3)) {  
                        enc4 = 64;  
                    }  
                    output = output + keyStr.charAt(enc1) + keyStr.charAt(enc2)  
                            + keyStr.charAt(enc3) + keyStr.charAt(enc4);  
                    chr1 = chr2 = chr3 = "";  
                    enc1 = enc2 = enc3 = enc4 = "";  
                } while (i < input.length);  

                return output;  
            }  
"""
