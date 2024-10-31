
import requests

cookies = {
    'JSESSIONID': 'DB43E7D56FCB0ACA102A060FAB06DDF5',
    'UNIQUECK': '4442600811304913214',
    'dtCookie': 'v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0',
    'ExWePre284': '!MfmiCBUd/ce7MayoFDBpXgYEZfUa2Pcv8lQ5lHkwisxaTM0dAgHx1OPUAWaVe3LzvyYKER5d5leOkMfDa/NEif/+hIMICWmQku4tQVGPznrZxxTPUekByBQqggFDsU4TKB/jReFhwqad7JccFUItl5D0qn+1L6Q=',
    'rxVisitor': '1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC',
    'dtSa': '-',
    'wfx_unq': 'EbaiK4Ndjg0kHJRO',
    'rxvt': '1730321189791|1730319311577',
    'dtPC': '3$519315208_122h29vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5',
    'AccessTypeRR': '4155888189',
    'Authorization': 'Bearer f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a344824104632a3c307f6af2da186df6c127484b6c370d20540e14e37c752e23e935a0b94846804c4ee000bd658dc2d6e8778a55e90f17fba79fa3f2b47c462acb42b97e7446503dfe3e5b6654ea21ab4e812473ae434600aae802f104567d69b6568d922a32b35be671ef7c258218381f454c3b6b4f3c86373.0c3560161391800692e976339fae91c7aa9d96fb1c82695e1abfaf8b4593f23d',
    'Cache-Control': 'no-store, no-cache',
    'Connection': 'keep-alive',
    'Content-Security-Policy': 'frame-ancestors self',
    'Content-Type': 'application/json',
    # 'Cookie': 'JSESSIONID=DB43E7D56FCB0ACA102A060FAB06DDF5; UNIQUECK=4442600811304913214; dtCookie=v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0; ExWePre284=!MfmiCBUd/ce7MayoFDBpXgYEZfUa2Pcv8lQ5lHkwisxaTM0dAgHx1OPUAWaVe3LzvyYKER5d5leOkMfDa/NEif/+hIMICWmQku4tQVGPznrZxxTPUekByBQqggFDsU4TKB/jReFhwqad7JccFUItl5D0qn+1L6Q=; rxVisitor=1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC; dtSa=-; wfx_unq=EbaiK4Ndjg0kHJRO; rxvt=1730321189791|1730319311577; dtPC=3$519315208_122h29vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0',
    'Expires': '0',
    'LogHeader': '{"logData":[]}',
    'Nonce': '68bed1f1aa546819',
    'Origin': 'https://atiendo.claro.com.co',
    'Pragma': 'no-cache',
    'Referer': 'https://atiendo.claro.com.co/pretups-ui/pretups-ui',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Signature': 'c37f06048a2ca990ad9ed307d896b6d4d6c5e830f1c5608b20d6791d3e204388',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'X-Content-Type-Options': 'nosniff',
    'X-FRAME-OPTIONS': 'SAMEORIGIN',
    'X-XSS-Protection': '1; mode=block',
    'country': 'CO',
    'language': 'es',
    'languageCode': '0',
    'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'x-dtpc': '3$519315208_122h29vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0',
}

json_data = {
    'data': {
        'msisdn2': '3994268254',
        'date': '30/10/24',
        'extnwcode': 'CC',
        'extrefnum': ' ',
        'language1': '0',
        'language2': '0',
        'selector': '50166',
        'amount': '2000',
        'pin': 'IshgsU8sCS8wDe2WmoeZxA==',
    },
}

response = requests.post(
    'https://atiendo.claro.com.co/pretups/rstapi/v1/claroServices/vas',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"data":{"msisdn2":"3994268254","date":"30/10/24","extnwcode":"CC","extrefnum":" ","language1":"0","language2":"0","selector":"50166","amount":"2000","pin":"IshgsU8sCS8wDe2WmoeZxA=="}}'
#response = requests.post(
#    'https://atiendo.claro.com.co/pretups/rstapi/v1/claroServices/vas',
#    cookies=cookies,
#    headers=headers,
#    data=data,
#)


cookies = {
    'luigiCookie': 'true',
    'dtCookie': 'v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0',
    'ExWePre284': '!MfmiCBUd/ce7MayoFDBpXgYEZfUa2Pcv8lQ5lHkwisxaTM0dAgHx1OPUAWaVe3LzvyYKER5d5leOkMfDa/NEif/+hIMICWmQku4tQVGPznrZxxTPUekByBQqggFDsU4TKB/jReFhwqad7JccFUItl5D0qn+1L6Q=',
    'rxVisitor': '1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC',
    'dtSa': '-',
    'wfx_unq': 'EbaiK4Ndjg0kHJRO',
    'rxvt': '1730321189791|1730319311577',
    'dtPC': '3$519315208_122h29vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0',
}

headers = {
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Language': 'es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5',
    'Connection': 'keep-alive',
    # 'Cookie': 'luigiCookie=true; dtCookie=v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0; ExWePre284=!MfmiCBUd/ce7MayoFDBpXgYEZfUa2Pcv8lQ5lHkwisxaTM0dAgHx1OPUAWaVe3LzvyYKER5d5leOkMfDa/NEif/+hIMICWmQku4tQVGPznrZxxTPUekByBQqggFDsU4TKB/jReFhwqad7JccFUItl5D0qn+1L6Q=; rxVisitor=1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC; dtSa=-; wfx_unq=EbaiK4Ndjg0kHJRO; rxvt=1730321189791|1730319311577; dtPC=3$519315208_122h29vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0',
    'Referer': 'https://atiendo.claro.com.co/pretups-ui/pretups-ui',
    'Sec-Fetch-Dest': 'image',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

response = requests.get(
    'https://atiendo.claro.com.co/pretups-ui/assets/images/failed_icons/png/cancel.png',
    cookies=cookies,
    headers=headers,
)


cookies = {
    'luigiCookie': 'true',
    'dtCookie': 'v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0',
    'ExWePre284': '!MfmiCBUd/ce7MayoFDBpXgYEZfUa2Pcv8lQ5lHkwisxaTM0dAgHx1OPUAWaVe3LzvyYKER5d5leOkMfDa/NEif/+hIMICWmQku4tQVGPznrZxxTPUekByBQqggFDsU4TKB/jReFhwqad7JccFUItl5D0qn+1L6Q=',
    'rxVisitor': '1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC',
    'dtSa': '-',
    'wfx_unq': 'EbaiK4Ndjg0kHJRO',
    'rxvt': '1730321189791|1730319311577',
    'dtPC': '3$519315208_122h-vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5',
    'Connection': 'keep-alive',
    'Content-Type': 'text/plain;charset=UTF-8',
    # 'Cookie': 'luigiCookie=true; dtCookie=v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0; ExWePre284=!MfmiCBUd/ce7MayoFDBpXgYEZfUa2Pcv8lQ5lHkwisxaTM0dAgHx1OPUAWaVe3LzvyYKER5d5leOkMfDa/NEif/+hIMICWmQku4tQVGPznrZxxTPUekByBQqggFDsU4TKB/jReFhwqad7JccFUItl5D0qn+1L6Q=; rxVisitor=1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC; dtSa=-; wfx_unq=EbaiK4Ndjg0kHJRO; rxvt=1730321189791|1730319311577; dtPC=3$519315208_122h-vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0',
    'Origin': 'https://atiendo.claro.com.co',
    'Referer': 'https://atiendo.claro.com.co/pretups-ui/pretups-ui',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'type': 'js3',
    'sn': 'v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0',
    'svrid': '3',
    'flavor': 'post',
    'vi': 'BEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0',
    'modifiedSince': '1729748199263',
    'rf': 'https://atiendo.claro.com.co/pretups-ui/pretups-ui',
    'bp': '3',
    'app': 'c4d19121783eb8bb',
    'crc': '2531045526',
    'en': 'zw2wluru',
    'end': '1',
}

data = '$a=1%7C29%7CRECARGAR%7CC%7Cx%7C1730319389789%7C1730319390017%7Cdn%7C467%7Cxu%7C%2Fpretups%2Frstapi%2Fv1%2FclaroServices%2Fvas%7Csvtrg%7C1%7Csvm%7Ci2%5Esk1%5Esh0%7Ctvtrg%7C1%7Ctvm%7Ci2%5Esk1%5Esh0%7Cxrt%7Cb1730319389792e0f0g0h0i0j0k0l201m201u618v318w318X400T-18z11I1M-1285912957V0W1%7Cxcs%7C205%7Cxce%7C205%7Crc%7C400%2C2%7C30%7C_event_%7C1730319389789%7C_vc_%7CV%7C228%5Epc%7CVCD%7C123%7CVCDS%7C0%7CVCS%7C263%7CVCO%7C263%7CVCI%7C0%7CVE%7C656%5Ep326%5Ep2500%5Eps%5Esimg.ng-tns-c20-4%7CS%7C210$rId=RID_568207253$rpId=-1690341430$domR=1730319318373$tvn=%2Fpretups-ui%2Fpretups-ui$tvt=1730319317178$tvm=i2%3Bk1%3Bh0$tvtrg=1$w=1912$h=911$sw=1920$sh=1080$ni=4g|10$url=https%3A%2F%2Fatiendo.claro.com.co%2Fpretups-ui%2Fpretups-ui$title=PreTUPS%20UI$latC=0$app=c4d19121783eb8bb$vi=BEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0$fId=519315208_122$v=10299241001084140$vID=1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC$time=1730319390177'

response = requests.post(
    'https://atiendo.claro.com.co/pretups-ui/rb_d8c7da74-67f6-4c13-beb4-ea4f6d60aae3',
    params=params,
    cookies=cookies,
    headers=headers,
    data=data,
)


cookies = {
    'luigiCookie': 'true',
    'dtCookie': 'v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0',
    'ExWePre284': '!MfmiCBUd/ce7MayoFDBpXgYEZfUa2Pcv8lQ5lHkwisxaTM0dAgHx1OPUAWaVe3LzvyYKER5d5leOkMfDa/NEif/+hIMICWmQku4tQVGPznrZxxTPUekByBQqggFDsU4TKB/jReFhwqad7JccFUItl5D0qn+1L6Q=',
    'rxVisitor': '1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC',
    'dtSa': '-',
    'wfx_unq': 'EbaiK4Ndjg0kHJRO',
    'rxvt': '1730321189791|1730319311577',
    'dtPC': '3$519315208_122h-vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5',
    'Connection': 'keep-alive',
    'Content-Type': 'text/plain;charset=UTF-8',
    # 'Cookie': 'luigiCookie=true; dtCookie=v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0; ExWePre284=!MfmiCBUd/ce7MayoFDBpXgYEZfUa2Pcv8lQ5lHkwisxaTM0dAgHx1OPUAWaVe3LzvyYKER5d5leOkMfDa/NEif/+hIMICWmQku4tQVGPznrZxxTPUekByBQqggFDsU4TKB/jReFhwqad7JccFUItl5D0qn+1L6Q=; rxVisitor=1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC; dtSa=-; wfx_unq=EbaiK4Ndjg0kHJRO; rxvt=1730321189791|1730319311577; dtPC=3$519315208_122h-vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0',
    'Origin': 'https://atiendo.claro.com.co',
    'Referer': 'https://atiendo.claro.com.co/pretups-ui/pretups-ui',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

params = {
    'type': 'js3',
    'sn': 'v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0',
    'svrid': '3',
    'flavor': 'post',
    'vi': 'BEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0',
    'modifiedSince': '1729748199263',
    'rf': 'https://atiendo.claro.com.co/pretups-ui/pretups-ui',
    'bp': '3',
    'app': 'c4d19121783eb8bb',
    'crc': '1516413724',
    'en': 'zw2wluru',
    'end': '1',
}

data = '$tvn=%2Fpretups-ui%2Fpretups-ui$tvt=1730319317178$tvm=i2%3Bk1%3Bh0$tvtrg=1$w=1912$h=911$sw=1920$sh=1080$ni=4g|10$rt=29-1730319315001%3Bhttps%3A%2F%2Fatiendo.claro.com.co%2Fpretups%2Frstapi%2Fv1%2FclaroServices%2Fvas%7Cb74791e0f0g0h0i0j0k0l201m201u618v318w318X400T-18z1I1M-1285912957V0W1%7Chttps%3A%2F%2Fatiendo.claro.com.co%2Fpretups-ui%2Fassets%2Fimages%2Ffailed_5Ficons%2Fpng%2Fcancel.png%7Cb74998e0f0g0h0i0j0k1l17m17u1051v751w751X200E2F2500O50P50Q34R34I7M632913259V0$url=https%3A%2F%2Fatiendo.claro.com.co%2Fpretups-ui%2Fpretups-ui$title=PreTUPS%20UI$latC=0$app=c4d19121783eb8bb$vi=BEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0$fId=519315208_122$v=10299241001084140$vID=1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC$time=1730319392204'

response = requests.post(
    'https://atiendo.claro.com.co/pretups-ui/rb_d8c7da74-67f6-4c13-beb4-ea4f6d60aae3',
    params=params,
    cookies=cookies,
    headers=headers,
    data=data,
)


cookies = {
    'JSESSIONID': 'DB43E7D56FCB0ACA102A060FAB06DDF5',
    'UNIQUECK': '4442600811304913214',
    'dtCookie': 'v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0',
    'ExWePre284': '!MfmiCBUd/ce7MayoFDBpXgYEZfUa2Pcv8lQ5lHkwisxaTM0dAgHx1OPUAWaVe3LzvyYKER5d5leOkMfDa/NEif/+hIMICWmQku4tQVGPznrZxxTPUekByBQqggFDsU4TKB/jReFhwqad7JccFUItl5D0qn+1L6Q=',
    'rxVisitor': '1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC',
    'dtSa': '-',
    'wfx_unq': 'EbaiK4Ndjg0kHJRO',
    'rxvt': '1730321189791|1730319311577',
    'dtPC': '3$519315208_122h-vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5',
    'AccessTypeRR': '4155888189',
    'Authorization': 'Bearer f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a344824104632a3c307f6af2da186df6c127484b6c370d20540e14e37c752e23e935a0b94846804c4ee000bd658dc2d6e8778a55e90f17fba79fa3f2b47c462acb42b97e7446503dfe3e5b6654ea21ab4e812473ae434600aae802f104567d69b6568d922a32b35be671ef7c258218381f454c3b6b4f3c86373.0c3560161391800692e976339fae91c7aa9d96fb1c82695e1abfaf8b4593f23d',
    'CLIENT_ID': 'a',
    'CLIENT_SECRET': 'a',
    'Cache-Control': 'no-store, no-cache',
    'Connection': 'keep-alive',
    'Content-Security-Policy': 'frame-ancestors self',
    'Content-Type': 'application/json',
    # 'Cookie': 'JSESSIONID=DB43E7D56FCB0ACA102A060FAB06DDF5; UNIQUECK=4442600811304913214; dtCookie=v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0; ExWePre284=!MfmiCBUd/ce7MayoFDBpXgYEZfUa2Pcv8lQ5lHkwisxaTM0dAgHx1OPUAWaVe3LzvyYKER5d5leOkMfDa/NEif/+hIMICWmQku4tQVGPznrZxxTPUekByBQqggFDsU4TKB/jReFhwqad7JccFUItl5D0qn+1L6Q=; rxVisitor=1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC; dtSa=-; wfx_unq=EbaiK4Ndjg0kHJRO; rxvt=1730321189791|1730319311577; dtPC=3$519315208_122h-vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0',
    'Expires': '0',
    'LogHeader': '{"logData":[]}',
    'Nonce': '6b0b4d993f22612c',
    'Origin': 'https://atiendo.claro.com.co',
    'Pragma': 'no-cache',
    'Referer': 'https://atiendo.claro.com.co/pretups-ui/pretups-ui',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Signature': '9569b375a3e4e43e621abc477a96f9e38172b16ef2d5dfe2086b45d76ec13cec',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'X-Content-Type-Options': 'nosniff',
    'X-FRAME-OPTIONS': 'SAMEORIGIN',
    'X-XSS-Protection': '1; mode=block',
    'country': 'CO',
    'language': 'es',
    'languageCode': '0',
    'scope': 'All',
    'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'refreshToken': 'f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a344824104632a3c307f6af2da186df6c127484b6c370d20540e14e37c752e23e935a0b94846804c4ee000bd658dc2d6e87603667d1a5673a0ea507d931da31c73c7962c7524b745f79f3f398e012b106ba18316dcb6e3d5da74bc37b785dc765e2404b27635f1a027d6392729382e3ecfaece147958df9e197.9c8b886b11288aaf10902ec7cfd6264cbc2467fc85df38597f3f0e1addc39005',
}

response = requests.post(
    'https://atiendo.claro.com.co/pretups/rstapi/v1/refreshTokenApi',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"refreshToken":"f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a344824104632a3c307f6af2da186df6c127484b6c370d20540e14e37c752e23e935a0b94846804c4ee000bd658dc2d6e87603667d1a5673a0ea507d931da31c73c7962c7524b745f79f3f398e012b106ba18316dcb6e3d5da74bc37b785dc765e2404b27635f1a027d6392729382e3ecfaece147958df9e197.9c8b886b11288aaf10902ec7cfd6264cbc2467fc85df38597f3f0e1addc39005"}'
#response = requests.post(
#    'https://atiendo.claro.com.co/pretups/rstapi/v1/refreshTokenApi',
#    cookies=cookies,
#    headers=headers,
#    data=data,
#)


cookies = {
    'JSESSIONID': 'DB43E7D56FCB0ACA102A060FAB06DDF5',
    'UNIQUECK': '4442600811304913214',
    'dtCookie': 'v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0',
    'ExWePre284': '!MfmiCBUd/ce7MayoFDBpXgYEZfUa2Pcv8lQ5lHkwisxaTM0dAgHx1OPUAWaVe3LzvyYKER5d5leOkMfDa/NEif/+hIMICWmQku4tQVGPznrZxxTPUekByBQqggFDsU4TKB/jReFhwqad7JccFUItl5D0qn+1L6Q=',
    'rxVisitor': '1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC',
    'dtSa': '-',
    'wfx_unq': 'EbaiK4Ndjg0kHJRO',
    'rxvt': '1730321189791|1730319311577',
    'dtPC': '3$519315208_122h-vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5',
    'AccessTypeRR': '4155888189',
    'Authorization': 'Bearer f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a34a5ce6b5b305fcf9d920b836c49d09b93858397d190d9a89c8a13123413e5c314c0d85226854c78d2d91d9fddf1a81153c4af1dc487aa1fe0dda1ca8a04d7a4e93362c5100d85e5445331575e5c4b6f00a008004bb336b0870d61df45874c186d84c42a576d7eca4bc11699d0c8f8c0dd945a4445e23d3fdd.f0b070acd3a043bf12b759eac9817f28a90ad3868d508b1b92a697b3cf088b65',
    'CLIENT_ID': 'a',
    'CLIENT_SECRET': 'a',
    'Cache-Control': 'no-store, no-cache',
    'Connection': 'keep-alive',
    'Content-Security-Policy': 'frame-ancestors self',
    'Content-Type': 'application/json',
    # 'Cookie': 'JSESSIONID=DB43E7D56FCB0ACA102A060FAB06DDF5; UNIQUECK=4442600811304913214; dtCookie=v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0; ExWePre284=!MfmiCBUd/ce7MayoFDBpXgYEZfUa2Pcv8lQ5lHkwisxaTM0dAgHx1OPUAWaVe3LzvyYKER5d5leOkMfDa/NEif/+hIMICWmQku4tQVGPznrZxxTPUekByBQqggFDsU4TKB/jReFhwqad7JccFUItl5D0qn+1L6Q=; rxVisitor=1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC; dtSa=-; wfx_unq=EbaiK4Ndjg0kHJRO; rxvt=1730321189791|1730319311577; dtPC=3$519315208_122h-vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0',
    'Expires': '0',
    'LogHeader': '{"logData":[]}',
    'Nonce': 'a56d6d58416943ad',
    'Origin': 'https://atiendo.claro.com.co',
    'Pragma': 'no-cache',
    'Referer': 'https://atiendo.claro.com.co/pretups-ui/pretups-ui',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Signature': '52309307c36769598517f81acb1ea11e09f71723c89aa4c7a9b9ae9f9c6e93f6',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'X-Content-Type-Options': 'nosniff',
    'X-FRAME-OPTIONS': 'SAMEORIGIN',
    'X-XSS-Protection': '1; mode=block',
    'country': 'CO',
    'language': 'es',
    'languageCode': '0',
    'scope': 'All',
    'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'refreshToken': 'f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a34a5ce6b5b305fcf9d920b836c49d09b93858397d190d9a89c8a13123413e5c314c0d85226854c78d2d91d9fddf1a811536f580f608696784d254f951237c3bd3b5b2afef67b146306d535477e7ecdfd778bd41a89aef83f425cb8bf9c3944643ab99b94e1ffbfd6761b4db960fd092bc74fc794b0954bb44e.205e2233ef66d6187c008c3ef5d07a5a8f81211ceb4d3f98cdfb0f32a29e86eb',
}

response = requests.post(
    'https://atiendo.claro.com.co/pretups/rstapi/v1/refreshTokenApi',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"refreshToken":"f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a34a5ce6b5b305fcf9d920b836c49d09b93858397d190d9a89c8a13123413e5c314c0d85226854c78d2d91d9fddf1a811536f580f608696784d254f951237c3bd3b5b2afef67b146306d535477e7ecdfd778bd41a89aef83f425cb8bf9c3944643ab99b94e1ffbfd6761b4db960fd092bc74fc794b0954bb44e.205e2233ef66d6187c008c3ef5d07a5a8f81211ceb4d3f98cdfb0f32a29e86eb"}'
#response = requests.post(
#    'https://atiendo.claro.com.co/pretups/rstapi/v1/refreshTokenApi',
#    cookies=cookies,
#    headers=headers,
#    data=data,
#)


cookies = {
    'JSESSIONID': 'DB43E7D56FCB0ACA102A060FAB06DDF5',
    'UNIQUECK': '4442600811304913214',
    'dtCookie': 'v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0',
    'ExWePre284': '!MfmiCBUd/ce7MayoFDBpXgYEZfUa2Pcv8lQ5lHkwisxaTM0dAgHx1OPUAWaVe3LzvyYKER5d5leOkMfDa/NEif/+hIMICWmQku4tQVGPznrZxxTPUekByBQqggFDsU4TKB/jReFhwqad7JccFUItl5D0qn+1L6Q=',
    'rxVisitor': '1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC',
    'dtSa': '-',
    'wfx_unq': 'EbaiK4Ndjg0kHJRO',
    'rxvt': '1730321189791|1730319311577',
    'dtPC': '3$519315208_122h-vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5',
    'AccessTypeRR': '4155888189',
    'Authorization': 'Bearer f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a34d1b8e4a01fe97c8c4adb19f050a5462a74bede31d39f526a9a852f913178ffd6bbd4bb232be4983d77ea202efc49f6107d763124835c26bc775981ff5fcbafc783325a0415138a37c16e502c6f1ee2b75658257a27abcdebc714cdca63d5debf4a0ac66cb845384cbd486a82ece6197f1d38618f998f1440.26bb990480b26e6f9b98df0673719f66945f22984782b4bbc86fd5c3100383c9',
    'CLIENT_ID': 'a',
    'CLIENT_SECRET': 'a',
    'Cache-Control': 'no-store, no-cache',
    'Connection': 'keep-alive',
    'Content-Security-Policy': 'frame-ancestors self',
    'Content-Type': 'application/json',
    # 'Cookie': 'JSESSIONID=DB43E7D56FCB0ACA102A060FAB06DDF5; UNIQUECK=4442600811304913214; dtCookie=v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0; ExWePre284=!MfmiCBUd/ce7MayoFDBpXgYEZfUa2Pcv8lQ5lHkwisxaTM0dAgHx1OPUAWaVe3LzvyYKER5d5leOkMfDa/NEif/+hIMICWmQku4tQVGPznrZxxTPUekByBQqggFDsU4TKB/jReFhwqad7JccFUItl5D0qn+1L6Q=; rxVisitor=1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC; dtSa=-; wfx_unq=EbaiK4Ndjg0kHJRO; rxvt=1730321189791|1730319311577; dtPC=3$519315208_122h-vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0',
    'Expires': '0',
    'LogHeader': '{"logData":[]}',
    'Nonce': 'b9258bff9b8dc55d',
    'Origin': 'https://atiendo.claro.com.co',
    'Pragma': 'no-cache',
    'Referer': 'https://atiendo.claro.com.co/pretups-ui/pretups-ui',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Signature': 'd6b48845a7bc15975b7ca27a9456ce1765920564a16b4c99b635acc5d1eecc86',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'X-Content-Type-Options': 'nosniff',
    'X-FRAME-OPTIONS': 'SAMEORIGIN',
    'X-XSS-Protection': '1; mode=block',
    'country': 'CO',
    'language': 'es',
    'languageCode': '0',
    'scope': 'All',
    'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'refreshToken': 'f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a34d1b8e4a01fe97c8c4adb19f050a5462a74bede31d39f526a9a852f913178ffd6bbd4bb232be4983d77ea202efc49f610cf9e2f6d364dadd8417913b638d6ff22936267bfec4bf0a771409a0b0227819b3ca3fe219e26bee00721ac55494d696fde3b2c8409d0deea66f56ab53a18ad0962044ffae9b60546.2850a4ba786506537370b72e98fdae76a2dee365b509e132edae2006fca72c98',
}

response = requests.post(
    'https://atiendo.claro.com.co/pretups/rstapi/v1/refreshTokenApi',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"refreshToken":"f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a34d1b8e4a01fe97c8c4adb19f050a5462a74bede31d39f526a9a852f913178ffd6bbd4bb232be4983d77ea202efc49f610cf9e2f6d364dadd8417913b638d6ff22936267bfec4bf0a771409a0b0227819b3ca3fe219e26bee00721ac55494d696fde3b2c8409d0deea66f56ab53a18ad0962044ffae9b60546.2850a4ba786506537370b72e98fdae76a2dee365b509e132edae2006fca72c98"}'
#response = requests.post(
#    'https://atiendo.claro.com.co/pretups/rstapi/v1/refreshTokenApi',
#    cookies=cookies,
#    headers=headers,
#    data=data,
#)


cookies = {
    'JSESSIONID': 'DB43E7D56FCB0ACA102A060FAB06DDF5',
    'UNIQUECK': '4442600811304913214',
    'dtCookie': 'v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0',
    'ExWePre284': '!MfmiCBUd/ce7MayoFDBpXgYEZfUa2Pcv8lQ5lHkwisxaTM0dAgHx1OPUAWaVe3LzvyYKER5d5leOkMfDa/NEif/+hIMICWmQku4tQVGPznrZxxTPUekByBQqggFDsU4TKB/jReFhwqad7JccFUItl5D0qn+1L6Q=',
    'rxVisitor': '1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC',
    'dtSa': '-',
    'wfx_unq': 'EbaiK4Ndjg0kHJRO',
    'rxvt': '1730321189791|1730319311577',
    'dtPC': '3$519315208_122h-vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5',
    'AccessTypeRR': '4155888189',
    'Authorization': 'Bearer f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a3493471b217603dbf6cffd7d3b7efc48918aaa2514a896c701989119c19bff0365f82470d17802a62c02121c30b255f2d5ef7b23277d07f1d0b83cf493c55dae89f443fd85971dfd58edfaad7f8ef7c84f0d037701c7bcfb2732553d676c8edfa3000f5807b39076e8fdb1dfa8cd8450297df9dfabdbb81f6c.2217ae5ab6ef38301ba068083e6608be47cf8ea35cbeff8e92f3d75198ae32c0',
    'CLIENT_ID': 'a',
    'CLIENT_SECRET': 'a',
    'Cache-Control': 'no-store, no-cache',
    'Connection': 'keep-alive',
    'Content-Security-Policy': 'frame-ancestors self',
    'Content-Type': 'application/json',
    # 'Cookie': 'JSESSIONID=DB43E7D56FCB0ACA102A060FAB06DDF5; UNIQUECK=4442600811304913214; dtCookie=v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0; ExWePre284=!MfmiCBUd/ce7MayoFDBpXgYEZfUa2Pcv8lQ5lHkwisxaTM0dAgHx1OPUAWaVe3LzvyYKER5d5leOkMfDa/NEif/+hIMICWmQku4tQVGPznrZxxTPUekByBQqggFDsU4TKB/jReFhwqad7JccFUItl5D0qn+1L6Q=; rxVisitor=1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC; dtSa=-; wfx_unq=EbaiK4Ndjg0kHJRO; rxvt=1730321189791|1730319311577; dtPC=3$519315208_122h-vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0',
    'Expires': '0',
    'LogHeader': '{"logData":[]}',
    'Nonce': 'c9ec5282396ac18d',
    'Origin': 'https://atiendo.claro.com.co',
    'Pragma': 'no-cache',
    'Referer': 'https://atiendo.claro.com.co/pretups-ui/pretups-ui',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Signature': '7abf40a1ab352f103aa5534fa418b48cc5219c0ba22b7bce8f1abdedbec4e3a6',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'X-Content-Type-Options': 'nosniff',
    'X-FRAME-OPTIONS': 'SAMEORIGIN',
    'X-XSS-Protection': '1; mode=block',
    'country': 'CO',
    'language': 'es',
    'languageCode': '0',
    'scope': 'All',
    'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'refreshToken': 'f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a3493471b217603dbf6cffd7d3b7efc48918aaa2514a896c701989119c19bff0365f82470d17802a62c02121c30b255f2d5c78b5f2f3177c9a357e284217315cd3ba47f3837746bb11172986a9425d2a6d249ce4ff5e5a5f6d51a4a92ed8b566579a845dac771f6c93b0e51585dc7bd460477b479565c59537c.dbaa2da146db4d2955aa04363ad971f5c516ec1f144a3b3f1fb0e0445af5c6b7',
}

response = requests.post(
    'https://atiendo.claro.com.co/pretups/rstapi/v1/refreshTokenApi',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"refreshToken":"f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a3493471b217603dbf6cffd7d3b7efc48918aaa2514a896c701989119c19bff0365f82470d17802a62c02121c30b255f2d5c78b5f2f3177c9a357e284217315cd3ba47f3837746bb11172986a9425d2a6d249ce4ff5e5a5f6d51a4a92ed8b566579a845dac771f6c93b0e51585dc7bd460477b479565c59537c.dbaa2da146db4d2955aa04363ad971f5c516ec1f144a3b3f1fb0e0445af5c6b7"}'
#response = requests.post(
#    'https://atiendo.claro.com.co/pretups/rstapi/v1/refreshTokenApi',
#    cookies=cookies,
#    headers=headers,
#    data=data,
#)


cookies = {
    'JSESSIONID': 'DB43E7D56FCB0ACA102A060FAB06DDF5',
    'UNIQUECK': '4442600811304913214',
    'dtCookie': 'v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0',
    'ExWePre284': '!MfmiCBUd/ce7MayoFDBpXgYEZfUa2Pcv8lQ5lHkwisxaTM0dAgHx1OPUAWaVe3LzvyYKER5d5leOkMfDa/NEif/+hIMICWmQku4tQVGPznrZxxTPUekByBQqggFDsU4TKB/jReFhwqad7JccFUItl5D0qn+1L6Q=',
    'rxVisitor': '1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC',
    'dtSa': '-',
    'wfx_unq': 'EbaiK4Ndjg0kHJRO',
    'rxvt': '1730321189791|1730319311577',
    'dtPC': '3$519315208_122h-vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5',
    'AccessTypeRR': '4155888189',
    'Authorization': 'Bearer f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a34fa3b99b25438cb6c5857b30f3e1d3451db47d359e082e1bc8308230a6bab1d70017730bc45a4141f3df11911bfbfd8916fb425b508dc371cb669c8311c7fb8085c60927473ef428ce864ea4c47df7a9dc2ec39b107a836d30861a4d115e8d00f0258c57cae26d8d5627e27110dc546b94c3bff5b95234482.6a88512d487e223cf724b3f5cc185487592e944c15a380f3b97fa756462f32c5',
    'CLIENT_ID': 'a',
    'CLIENT_SECRET': 'a',
    'Cache-Control': 'no-store, no-cache',
    'Connection': 'keep-alive',
    'Content-Security-Policy': 'frame-ancestors self',
    'Content-Type': 'application/json',
    # 'Cookie': 'JSESSIONID=DB43E7D56FCB0ACA102A060FAB06DDF5; UNIQUECK=4442600811304913214; dtCookie=v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0; ExWePre284=!MfmiCBUd/ce7MayoFDBpXgYEZfUa2Pcv8lQ5lHkwisxaTM0dAgHx1OPUAWaVe3LzvyYKER5d5leOkMfDa/NEif/+hIMICWmQku4tQVGPznrZxxTPUekByBQqggFDsU4TKB/jReFhwqad7JccFUItl5D0qn+1L6Q=; rxVisitor=1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC; dtSa=-; wfx_unq=EbaiK4Ndjg0kHJRO; rxvt=1730321189791|1730319311577; dtPC=3$519315208_122h-vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0',
    'Expires': '0',
    'LogHeader': '{"logData":[]}',
    'Nonce': 'ace0887a305a1d81',
    'Origin': 'https://atiendo.claro.com.co',
    'Pragma': 'no-cache',
    'Referer': 'https://atiendo.claro.com.co/pretups-ui/pretups-ui',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Signature': '53513a716405521a2644902faf5895d2745c195d7b1c6cc5fb065ad1aa0c9c99',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'X-Content-Type-Options': 'nosniff',
    'X-FRAME-OPTIONS': 'SAMEORIGIN',
    'X-XSS-Protection': '1; mode=block',
    'country': 'CO',
    'language': 'es',
    'languageCode': '0',
    'scope': 'All',
    'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'refreshToken': 'f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a34fa3b99b25438cb6c5857b30f3e1d3451db47d359e082e1bc8308230a6bab1d70017730bc45a4141f3df11911bfbfd891cff0d02937da6eeb32e3805add8e77b2f361fd03a1835ff3f66c47c2c4430e2f1195360b0e19b2a78a08dc4cb7f9759fc7bee70ece43471d59d88558d6c53f60a4b7acef5a92d64e.6539eadbda5fe2297b6c8be659dc0b37c051b6702f1244c3b4239dac63809ed8',
}

response = requests.post(
    'https://atiendo.claro.com.co/pretups/rstapi/v1/refreshTokenApi',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"refreshToken":"f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a34fa3b99b25438cb6c5857b30f3e1d3451db47d359e082e1bc8308230a6bab1d70017730bc45a4141f3df11911bfbfd891cff0d02937da6eeb32e3805add8e77b2f361fd03a1835ff3f66c47c2c4430e2f1195360b0e19b2a78a08dc4cb7f9759fc7bee70ece43471d59d88558d6c53f60a4b7acef5a92d64e.6539eadbda5fe2297b6c8be659dc0b37c051b6702f1244c3b4239dac63809ed8"}'
#response = requests.post(
#    'https://atiendo.claro.com.co/pretups/rstapi/v1/refreshTokenApi',
#    cookies=cookies,
#    headers=headers,
#    data=data,
#)


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5',
    'AccessTypeRR': '4155888189',
    'Authorization': 'Bearer f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a347e171431b7808ede0efb0e341487d7860f8cd6ff90ccc2a9f37df087811a394687b3606205a0f166549fef63128a20a72c8f41b0e33282ded48a42ade16d0f20a4d5fb2d4697db65bbb960bbf002a1253b3e6815db83906add288de87b85f539f17560c654da5bcbe9a07e92028954f4252a87afc1db82b8.565cfeb8303a5b4f91362aef85d4776ba2db996c6c622953f782959afabf8bb2',
    'CLIENT_ID': 'a',
    'CLIENT_SECRET': 'a',
    'Cache-Control': 'no-store, no-cache',
    'Connection': 'keep-alive',
    'Content-Security-Policy': 'frame-ancestors self',
    'Content-Type': 'application/json',
    'Cookie': 'JSESSIONID=DB43E7D56FCB0ACA102A060FAB06DDF5; UNIQUECK=4442600811304913214; dtCookie=v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0; ExWePre284=!MfmiCBUd/ce7MayoFDBpXgYEZfUa2Pcv8lQ5lHkwisxaTM0dAgHx1OPUAWaVe3LzvyYKER5d5leOkMfDa/NEif/+hIMICWmQku4tQVGPznrZxxTPUekByBQqggFDsU4TKB/jReFhwqad7JccFUItl5D0qn+1L6Q=; dtSa=-; wfx_unq=EbaiK4Ndjg0kHJRO; rxvt=1730321189791|1730319311577; dtPC=3$519315208_122h-vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0; 1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC',
    'Expires': '0',
    'LogHeader': '{"logData":[]}',
    'Nonce': '965c84bc3ab503f0',
    'Origin': 'https://atiendo.claro.com.co',
    'Pragma': 'no-cache',
    'Referer': 'https://atiendo.claro.com.co/pretups-ui/pretups-ui',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Signature': '60f4199f641d40f55f9072cb33bacd3020dc9c12d1b5be7b5b3c2020c483478c',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'X-Content-Type-Options': 'nosniff',
    'X-FRAME-OPTIONS': 'SAMEORIGIN',
    'X-XSS-Protection': '1; mode=block',
    'country': 'CO',
    'language': 'es',
    'languageCode': '0',
    'scope': 'All',
    'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'refreshToken': 'f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a347e171431b7808ede0efb0e341487d7860f8cd6ff90ccc2a9f37df087811a394687b3606205a0f166549fef63128a20a7a13d53f4919a45ef9b8d445237a42f7dd515b62b5c35e13b98432a85e21c35949718a4192ab51150db7e7ff22059d7c0d5d71c202ae234cfb4312b2acb1b2a03050522102b4b358d.1652434ad7975f674f6c2919b1e0b388298023d8df0e12e57a7b08c200a85288',
}

response = requests.post('https://atiendo.claro.com.co/pretups/rstapi/v1/refreshTokenApi', headers=headers, json=json_data)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"refreshToken":"f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a347e171431b7808ede0efb0e341487d7860f8cd6ff90ccc2a9f37df087811a394687b3606205a0f166549fef63128a20a7a13d53f4919a45ef9b8d445237a42f7dd515b62b5c35e13b98432a85e21c35949718a4192ab51150db7e7ff22059d7c0d5d71c202ae234cfb4312b2acb1b2a03050522102b4b358d.1652434ad7975f674f6c2919b1e0b388298023d8df0e12e57a7b08c200a85288"}'
#response = requests.post('https://atiendo.claro.com.co/pretups/rstapi/v1/refreshTokenApi', headers=headers, data=data)


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5',
    'AccessTypeRR': '4155888189',
    'Authorization': 'Bearer f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a34a757198f7bd1cecf0764f739acc48c17ddf8bf35571366364c38743a9a6d1369f1aec2cc5e434b685c31e64feb50345fe6030460cb03d7b0e6523b51678d3b1d41f07cda575e0a6951e2e01776a600b468c74323906ef3c8a5a47c6c38b1036b896bd18209881836ab8fec8b11561aeba5d5d30fcaf7d475.6cf2614fed55e78d0e9fa59eabddd2fad71c9e5a097bf2c26d2caae1c348af21',
    'CLIENT_ID': 'a',
    'CLIENT_SECRET': 'a',
    'Cache-Control': 'no-store, no-cache',
    'Connection': 'keep-alive',
    'Content-Security-Policy': 'frame-ancestors self',
    'Content-Type': 'application/json',
    'Cookie': 'JSESSIONID=DB43E7D56FCB0ACA102A060FAB06DDF5; UNIQUECK=4442600811304913214; dtCookie=v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0; ExWePre284=!MfmiCBUd/ce7MayoFDBpXgYEZfUa2Pcv8lQ5lHkwisxaTM0dAgHx1OPUAWaVe3LzvyYKER5d5leOkMfDa/NEif/+hIMICWmQku4tQVGPznrZxxTPUekByBQqggFDsU4TKB/jReFhwqad7JccFUItl5D0qn+1L6Q=; dtSa=-; wfx_unq=EbaiK4Ndjg0kHJRO; rxvt=1730321189791|1730319311577; dtPC=3$519315208_122h-vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0; 1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC',
    'Expires': '0',
    'LogHeader': '{"logData":[]}',
    'Nonce': 'c83778f36ab3c6ab',
    'Origin': 'https://atiendo.claro.com.co',
    'Pragma': 'no-cache',
    'Referer': 'https://atiendo.claro.com.co/pretups-ui/pretups-ui',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Signature': 'ac485c3e37dac8a81676e01bb013249538f4af0b667cffd6421c5292596cadd3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'X-Content-Type-Options': 'nosniff',
    'X-FRAME-OPTIONS': 'SAMEORIGIN',
    'X-XSS-Protection': '1; mode=block',
    'country': 'CO',
    'language': 'es',
    'languageCode': '0',
    'scope': 'All',
    'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'refreshToken': 'f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a34a757198f7bd1cecf0764f739acc48c17ddf8bf35571366364c38743a9a6d1369f1aec2cc5e434b685c31e64feb50345f5b922a4a8eccea31c4e918ec561562393c94dc95887a2e192e7c9411e7bd4f246e113ed75bf880c429263636a42f77133a5632da028b6a2ce57b7c359f278898d40d59356c39207a.8e1fbb74ead9616b01c63929451be05869884c037cd70d13fd2f5645c0244307',
}

response = requests.post('https://atiendo.claro.com.co/pretups/rstapi/v1/refreshTokenApi', headers=headers, json=json_data)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"refreshToken":"f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a34a757198f7bd1cecf0764f739acc48c17ddf8bf35571366364c38743a9a6d1369f1aec2cc5e434b685c31e64feb50345f5b922a4a8eccea31c4e918ec561562393c94dc95887a2e192e7c9411e7bd4f246e113ed75bf880c429263636a42f77133a5632da028b6a2ce57b7c359f278898d40d59356c39207a.8e1fbb74ead9616b01c63929451be05869884c037cd70d13fd2f5645c0244307"}'
#response = requests.post('https://atiendo.claro.com.co/pretups/rstapi/v1/refreshTokenApi', headers=headers, data=data)


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5',
    'AccessTypeRR': '4155888189',
    'Authorization': 'Bearer f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a34f03ac36784b2335f03a096dc4a25c69500558a408baddad03879e39939965bfb56cff953e49852d8478a4000465b0662f205d97d0f03f3e71811abba97b1497f8d222ddc593e2cff08a6abde5d941948ebf87b3ad9c847e0d328914e2f5e28c19f4678085be020131212a11c12faba0cf13ddc2c3bb24309.6e61fda11060af708ecad016bc95d5c311fc38bea07ab3830ed3a77e5d7328f4',
    'CLIENT_ID': 'a',
    'CLIENT_SECRET': 'a',
    'Cache-Control': 'no-store, no-cache',
    'Connection': 'keep-alive',
    'Content-Security-Policy': 'frame-ancestors self',
    'Content-Type': 'application/json',
    'Cookie': 'JSESSIONID=DB43E7D56FCB0ACA102A060FAB06DDF5; UNIQUECK=4442600811304913214; dtCookie=v_4_srv_3_sn_0757B95B46323C1C93EE5A6BBE32B438_perc_100000_ol_0_mul_1_app-3Ac4d19121783eb8bb_1_rcs-3Acss_0; ExWePre284=!MfmiCBUd/ce7MayoFDBpXgYEZfUa2Pcv8lQ5lHkwisxaTM0dAgHx1OPUAWaVe3LzvyYKER5d5leOkMfDa/NEif/+hIMICWmQku4tQVGPznrZxxTPUekByBQqggFDsU4TKB/jReFhwqad7JccFUItl5D0qn+1L6Q=; dtSa=-; wfx_unq=EbaiK4Ndjg0kHJRO; rxvt=1730321189791|1730319311577; dtPC=3$519315208_122h-vBEBALIMTEQKEJTRLDRTVIPFDMPFHRMWH-0e0; 1730319311576L4D91SSUSV5GB5LD3UOOR2LN57N5UPNC',
    'Expires': '0',
    'LogHeader': '{"logData":[]}',
    'Nonce': 'b8d62aabb11f055d',
    'Origin': 'https://atiendo.claro.com.co',
    'Pragma': 'no-cache',
    'Referer': 'https://atiendo.claro.com.co/pretups-ui/pretups-ui',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Signature': 'a82e8cc2d4e4cd81a0ffa3700e30146371a4ed7f34e73f852511764619b9c486',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
    'X-Content-Type-Options': 'nosniff',
    'X-FRAME-OPTIONS': 'SAMEORIGIN',
    'X-XSS-Protection': '1; mode=block',
    'country': 'CO',
    'language': 'es',
    'languageCode': '0',
    'scope': 'All',
    'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'refreshToken': 'f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a34f03ac36784b2335f03a096dc4a25c69500558a408baddad03879e39939965bfb56cff953e49852d8478a4000465b0662f66f486660ebd785aaffdc71938c274305191ba00b2b852f5a661d656e23be1d0ce4f827eccb5ff962c7944778a959d9654ea0cee65f5a11435fb85238f82240eec4f5a1cff5c7f3.a96e9d61612653cbf14e8a72b1e302cced0c7ddccd281b93094925a03f4c2706',
}

response = requests.post('https://atiendo.claro.com.co/pretups/rstapi/v1/refreshTokenApi', headers=headers, json=json_data)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"refreshToken":"f7ebdf1d78e7da6a7681ea64c4b06b5fb3e1804c290bdfe003766c5ad41d4d53.c3dffac20ac87aef3fbf677359d13a34f03ac36784b2335f03a096dc4a25c69500558a408baddad03879e39939965bfb56cff953e49852d8478a4000465b0662f66f486660ebd785aaffdc71938c274305191ba00b2b852f5a661d656e23be1d0ce4f827eccb5ff962c7944778a959d9654ea0cee65f5a11435fb85238f82240eec4f5a1cff5c7f3.a96e9d61612653cbf14e8a72b1e302cced0c7ddccd281b93094925a03f4c2706"}'
#response = requests.post('https://atiendo.claro.com.co/pretups/rstapi/v1/refreshTokenApi', headers=headers, data=data)