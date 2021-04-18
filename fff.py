import base64
import json

wrong_password = 'abababababa'


# base64 解码 需要是4的倍数
def base64decode(s):
    # transtab = str.maketrans('-_', '+/')
    # s = s.translate(transtab)
    if len(s) % 4 != 0:
        s = s + (4 - len(s) % 4) * '='
    return base64.urlsafe_b64decode(s.encode())


def decode_ss(ss):
    code_base64 = ss[5:ss.find('@')]
    method_pwd = base64decode(code_base64)
    method_b, pwd_b = method_pwd.split(b':', 1)
    server = ss[ss.find('@') + 1:ss.rfind(':')]
    if ss.find('#') == -1:
        port = ss[ss.rfind(':') + 1:]
    else:
        port = ss[ss.rfind(':') + 1:ss.find('#')]
    ss_conf = {'server': server, 'server_port': int(port),
               'password': pwd_b.decode(), 'method': method_b.decode()}
    print(json.dumps(ss_conf, indent=4))

    pwd_base64 = base64.urlsafe_b64encode(pwd_b)

    ssr = [server, port, 'origin', method_b.decode(), 'plain',
           pwd_base64.decode()]
    ssrlink = ':'.join(ssr) + '/?obfsparam=&protoparam=&remarks='
    ssrlink_base64 = base64.urlsafe_b64encode(ssrlink.encode())
    ssrlink_output = 'ssr://' + ssrlink_base64.decode()
    print(ssrlink_output)


def decode_ssr(ssr, group='', remarks='', out_date=False):
    base_connection_url = base64decode(ssr[6:])
    server, server_port, protocol, method, obfs, other = base_connection_url.decode().split(':')
    password_base64, param_base64 = other.split("/?")
    password = base64decode(password_base64)
    params = param_base64.split("&")

    key = {}
    for param in params:
        k, v = param.split("=", 1)
        if v:
            key[k] = v
    print(key)
    obfsparam_base64 = key.get('obfsparam')
    protoparam_base64 = key.get('protoparam')
    if obfsparam_base64:
        obfsparam = base64decode(obfsparam_base64)
    if protoparam_base64:
        protoparam = base64decode(protoparam_base64)
    if out_date:
        password_base64 = base64.b64encode(wrong_password.encode())
    ssr = [server, server_port, protocol, method, obfs, password_base64]

    remarks_base64 = str(base64.b64encode(remarks.encode('utf-8')), "utf-8")
    group_base64 = str(base64.b64encode(group.encode('utf-8')), "utf-8")
    ssrlink = ':'.join(ssr) + '/?obfsparam={}&protoparam={}&remarks={}&group={}'.format(obfsparam_base64,
                                                                                        protoparam_base64,
                                                                                        remarks_base64, group_base64)
    ssrlink_base64 = base64.urlsafe_b64encode(ssrlink.encode())
    ssrlink_output = 'ssr://' + ssrlink_base64.decode()
    return ssrlink_output


def main():
    s = 'ssr://aGs0LnN1Yndsa2oubGluazo3MDg1OmF1dGhfYWVzMTI4X21kNTpjaGFjaGEyMC1pZXRmOnRsczEuMl90aWNrZXRfYXV0aDpZMlZXUm5wb2VqUS8_b2Jmc3BhcmFtPVpHbHpZM1Z6YzJsdmJuTXVZWEJ3YkdVdVkyOXQmcHJvdG9wYXJhbT1NVGMwTlRZNlozRjZiVGhTZFhKYVRXUjVibEZRUjNOTlMwdG1SMmxyVjBSMFRWUk9WbTAmcmVtYXJrcz01WW1wNUwyWjVyV0I2WWVQNzd5YU1qZzVMalJIUWcmZ3JvdXA9VTNCbFpXVG52WkhudTV6bnA1SG1pb0EmdWRwcG9ydD0wJnVvdD0w'
    is_ss = s.find('ss://')
    is_ssr = s.find('ssr://')
    if is_ss != -1:
        ss = s[is_ss:].strip()
        decode_ss(ss)
    elif is_ssr != -1:
        ssr = s[is_ssr:].strip()
        decode_ssr(ssr)
    else:
        print('链接格式不正确！')


if __name__ == '__main__':
    temp = base64decode(
        'c3NyOi8vYUdzMExuTjFZbmRzYTJvdWJHbHVhem8zTURnMU9tRjFkR2hmWVdWek1USTRYMjFrTlRwamFHRmphR0V5TUMxcFpYUm1PblJzY3pFdU1sOTBhV05yWlhSZllYVjBhRHBaTWxaWFVtNXdiMlZxVVM4X2IySm1jM0JoY21GdFBWcEhiSHBaTTFaNll6SnNkbUp1VFhWWldFSjNZa2RWZFZreU9YUW1jSEp2ZEc5d1lYSmhiVDFOVkdNd1RsUlpObG96UmpaaVZHaFRaRmhLWVZSWFVqVmliRVpSVWpOT1RsTXdkRzFTTW14eVZqQlNNRlJXVWs5V2JUQW1jbVZ0WVhKcmN6MDJUQzFJTlhCNVpqVndaVEkyV21Vd056ZDVZVTFxUVhsTmFUQjNUWGt3ZDAxUkptZHliM1Z3UFZVelFteGFWMVJ1ZGxwSWJuVTFlbTV3TlVodGFXOUJKblZrY0hCdmNuUTlNQ1oxYjNROU1BCnNzcjovL2FHczBMbk4xWW5kc2Eyb3ViR2x1YXpvM01EZzFPbUYxZEdoZllXVnpNVEk0WDIxa05UcGphR0ZqYUdFeU1DMXBaWFJtT25Sc2N6RXVNbDkwYVdOclpYUmZZWFYwYURwWk1sWlhVbTV3YjJWcVVTOF9iMkptYzNCaGNtRnRQVnBIYkhwWk0xWjZZekpzZG1KdVRYVlpXRUozWWtkVmRWa3lPWFFtY0hKdmRHOXdZWEpoYlQxTlZHTXdUbFJaTmxvelJqWmlWR2hUWkZoS1lWUlhValZpYkVaUlVqTk9UbE13ZEcxU01teHlWakJTTUZSV1VrOVdiVEFtY21WdFlYSnJjejAxV1cxd05Vd3lXalZ5VjBJMldXVlFOemQ1WVUxcVp6Uk1hbXQ2VWpCSkptZHliM1Z3UFZVelFteGFWMVJ1ZGxwSWJuVTFlbTV3TlVodGFXOUJKblZrY0hCdmNuUTlNQ1oxYjNROU1BCnNzcjovL2FHczBMbk4xWW5kc2Eyb3ViR2x1YXpvM01EZzFPbUYxZEdoZllXVnpNVEk0WDIxa05UcGphR0ZqYUdFeU1DMXBaWFJtT25Sc2N6RXVNbDkwYVdOclpYUmZZWFYwYURwWk1sWlhVbTV3YjJWcVVTOF9iMkptYzNCaGNtRnRQVnBIYkhwWk0xWjZZekpzZG1KdVRYVlpXRUozWWtkVmRWa3lPWFFtY0hKdmRHOXdZWEpoYlQxTlZHTXdUbFJaTmxvelJqWmlWR2hUWkZoS1lWUlhValZpYkVaUlVqTk9UbE13ZEcxU01teHlWakJTTUZSV1VrOVdiVEFtY21WdFlYSnJjejAxTjNWME5reFROVFZhZVhjMVdqSkJOemQ1WVdGSVVqQmpTRTAyVEhrNWVtTkhWbXhhU0dSellUSnZkVmt5ZURGWlp5Wm5jbTkxY0QxVk0wSnNXbGRVYm5aYVNHNTFOWHB1Y0RWSWJXbHZRU1oxWkhCd2IzSjBQVEFtZFc5MFBUQQpzc3I6Ly9jeTFxY0RFdWMzVmlkMnhyYWk1c2FXNXJPamd3TnpNNllYVjBhRjloWlhNeE1qaGZiV1ExT21Ob1lXTm9ZVEl3TFdsbGRHWTZkR3h6TVM0eVgzUnBZMnRsZEY5aGRYUm9PbGt5VmxkU2JuQnZaV3BSTHo5dlltWnpjR0Z5WVcwOVdrZHNlbGt6Vm5wak1teDJZbTVOZFZsWVFuZGlSMVYxV1RJNWRDWndjbTkwYjNCaGNtRnRQVTFVWXpCT1ZGazJXak5HTm1KVWFGTmtXRXBoVkZkU05XSnNSbEZTTTA1T1V6QjBiVkl5YkhKV01GSXdWRlpTVDFadE1DWnlaVzFoY210elBWY3RiVGRvVDIxSWExWXphVzFKV0cxc05saHRia3QzZUU5cFFrOWFXRkp0WWtkc05FbElkMmRSVjBwc1lsZEdWV1JuSm1keWIzVndQVlV6UW14YVYxUnVkbHBJYm5VMWVtNXdOVWh0YVc5QkpuVmtjSEJ2Y25ROU1DWjFiM1E5TUEKc3NyOi8vY3kxcWNESXVjM1ZpZDJ4cmFpNXNhVzVyT2pnd056TTZZWFYwYUY5aFpYTXhNamhmYldRMU9tTm9ZV05vWVRJd0xXbGxkR1k2ZEd4ek1TNHlYM1JwWTJ0bGRGOWhkWFJvT2xreVZsZFNibkJ2WldwUkx6OXZZbVp6Y0dGeVlXMDlXa2RzZWxrelZucGpNbXgyWW01TmRWbFlRbmRpUjFWMVdUSTVkQ1p3Y205MGIzQmhjbUZ0UFUxVVl6Qk9WRmsyV2pOR05tSlVhRk5rV0VwaFZGZFNOV0pzUmxGU00wNU9VekIwYlZJeWJISldNRkl3VkZaU1QxWnRNQ1p5WlcxaGNtdHpQVmN0YlRkb1QyMUlhMVl6YVcxSldHMXNObGh0Ymt0M2VVOXBRazlhV0ZKdFlrZHNORWxJZDJkUlYwcHNZbGRHVldSbkptZHliM1Z3UFZVelFteGFWMVJ1ZGxwSWJuVTFlbTV3TlVodGFXOUJKblZrY0hCdmNuUTlNQ1oxYjNROU1BCnNzcjovL2N5MXFjRE11YzNWaWQyeHJhaTVzYVc1ck9qZ3dOek02WVhWMGFGOWhaWE14TWpoZmJXUTFPbU5vWVdOb1lUSXdMV2xsZEdZNmRHeHpNUzR5WDNScFkydGxkRjloZFhSb09sa3lWbGRTYm5CdlpXcFJMejl2WW1aemNHRnlZVzA5V2tkc2Vsa3pWbnBqTW14MlltNU5kVmxZUW5kaVIxVjFXVEk1ZENad2NtOTBiM0JoY21GdFBVMVVZekJPVkZrMldqTkdObUpVYUZOa1dFcGhWRmRTTldKc1JsRlNNMDVPVXpCMGJWSXliSEpXTUZJd1ZGWlNUMVp0TUNaeVpXMWhjbXR6UFZjdGJUZG9UMjFJYTFZemFXMUpXRzFzTmxodGJrdDNlazlwUWs5YVdGSnRZa2RzTkVsSWQyZFJWMHBzWWxkR1ZXUm5KbWR5YjNWd1BWVXpRbXhhVjFSdWRscEliblUxZW01d05VaHRhVzlCSm5Wa2NIQnZjblE5TUNaMWIzUTlNQQpzc3I6Ly9jeTFxY0RRdWMzVmlkMnhyYWk1c2FXNXJPamd3TnpNNllYVjBhRjloWlhNeE1qaGZiV1ExT21Ob1lXTm9ZVEl3TFdsbGRHWTZkR3h6TVM0eVgzUnBZMnRsZEY5aGRYUm9PbGt5VmxkU2JuQnZaV3BSTHo5dlltWnpjR0Z5WVcwOVdrZHNlbGt6Vm5wak1teDJZbTVOZFZsWVFuZGlSMVYxV1RJNWRDWndjbTkwYjNCaGNtRnRQVTFVWXpCT1ZGazJXak5HTm1KVWFGTmtXRXBoVkZkU05XSnNSbEZTTTA1T1V6QjBiVkl5YkhKV01GSXdWRlpTVDFadE1DWnlaVzFoY210elBWY3RiVGRvVDIxSWExWXphVzFKV0cxc05saHRia3QzTUU5cFFrOWFXRkp0WWtkc05FbElkMmRSVjBwc1lsZEdWV1JuSm1keWIzVndQVlV6UW14YVYxUnVkbHBJYm5VMWVtNXdOVWh0YVc5QkpuVmtjSEJ2Y25ROU1DWjFiM1E5TUEKc3NyOi8vY3kxcWNEVXVjM1ZpZDJ4cmFpNXNhVzVyT2pnd056TTZZWFYwYUY5aFpYTXhNamhmYldRMU9tTm9ZV05vWVRJd0xXbGxkR1k2ZEd4ek1TNHlYM1JwWTJ0bGRGOWhkWFJvT2xreVZsZFNibkJ2WldwUkx6OXZZbVp6Y0dGeVlXMDlXa2RzZWxrelZucGpNbXgyWW01TmRWbFlRbmRpUjFWMVdUSTVkQ1p3Y205MGIzQmhjbUZ0UFUxVVl6Qk9WRmsyV2pOR05tSlVhRk5rV0VwaFZGZFNOV0pzUmxGU00wNU9VekIwYlZJeWJISldNRkl3VkZaU1QxWnRNQ1p5WlcxaGNtdHpQVmN0YlRkb1QyMUlhMVl6YVcxSldHMXNObGh0Ymt0M01VOXBRazlhV0ZKdFlrZHNORWxJZDJkUlYwcHNZbGRHVldSbkptZHliM1Z3UFZVelFteGFWMVJ1ZGxwSWJuVTFlbTV3TlVodGFXOUJKblZrY0hCdmNuUTlNQ1oxYjNROU1BCnNzcjovL2N5MXFjRFl1YzNWaWQyeHJhaTVzYVc1ck9qZ3dOek02WVhWMGFGOWhaWE14TWpoZmJXUTFPbU5vWVdOb1lUSXdMV2xsZEdZNmRHeHpNUzR5WDNScFkydGxkRjloZFhSb09sa3lWbGRTYm5CdlpXcFJMejl2WW1aemNHRnlZVzA5V2tkc2Vsa3pWbnBqTW14MlltNU5kVmxZUW5kaVIxVjFXVEk1ZENad2NtOTBiM0JoY21GdFBVMVVZekJPVkZrMldqTkdObUpVYUZOa1dFcGhWRmRTTldKc1JsRlNNMDVPVXpCMGJWSXliSEpXTUZJd1ZGWlNUMVp0TUNaeVpXMWhjbXR6UFZjdGJUZG9UMjFJYTFZemFXMUpXRzFzTmxodGJrdDNNazlwUWs5YVdGSnRZa2RzTkVsSWQyZFJWMHBzWWxkR1ZXUm5KbWR5YjNWd1BWVXpRbXhhVjFSdWRscEliblUxZW01d05VaHRhVzlCSm5Wa2NIQnZjblE5TUNaMWIzUTlNQQpzc3I6Ly9jeTF5ZFRFdWMzVmlkMnhyYWk1c2FXNXJPamt3T0RFNllYVjBhRjloWlhNeE1qaGZiV1ExT21Ob1lXTm9ZVEl3TFdsbGRHWTZkR3h6TVM0eVgzUnBZMnRsZEY5aGRYUm9PbGt5VmxkU2JuQnZaV3BSTHo5dlltWnpjR0Z5WVcwOVdrZHNlbGt6Vm5wak1teDJZbTVOZFZsWVFuZGlSMVYxV1RJNWRDWndjbTkwYjNCaGNtRnRQVTFVWXpCT1ZGazJXak5HTm1KVWFGTmtXRXBoVkZkU05XSnNSbEZTTTA1T1V6QjBiVkl5YkhKV01GSXdWRlpTVDFadE1DWnlaVzFoY210elBWY3RiVGRvVDIxSWExWXphVzFKV0d0Mk5GUnVkbHBtYld4eE9IaFBhelZzWkVkYWMyRllaMmRtUTBKRFVXdE5KbWR5YjNWd1BWVXpRbXhhVjFSdWRscEliblUxZW01d05VaHRhVzlCSm5Wa2NIQnZjblE5TUNaMWIzUTlNQQpzc3I6Ly9jeTF5ZFRJdWMzVmlkMnhyYWk1c2FXNXJPamt3T0RFNllYVjBhRjloWlhNeE1qaGZiV1ExT21Ob1lXTm9ZVEl3TFdsbGRHWTZkR3h6TVM0eVgzUnBZMnRsZEY5aGRYUm9PbGt5VmxkU2JuQnZaV3BSTHo5dlltWnpjR0Z5WVcwOVdrZHNlbGt6Vm5wak1teDJZbTVOZFZsWVFuZGlSMVYxV1RJNWRDWndjbTkwYjNCaGNtRnRQVTFVWXpCT1ZGazJXak5HTm1KVWFGTmtXRXBoVkZkU05XSnNSbEZTTTA1T1V6QjBiVkl5YkhKV01GSXdWRlpTVDFadE1DWnlaVzFoY210elBWY3RiVGRvVDIxSWExWXphVzFKV0d0Mk5GUnVkbHBtYld4eE9IbFBhelZzWkVkYWMyRllaMmRtUTBKRFVXdE5KbWR5YjNWd1BWVXpRbXhhVjFSdWRscEliblUxZW01d05VaHRhVzlCSm5Wa2NIQnZjblE5TUNaMWIzUTlNQQpzc3I6Ly9jeTF5ZFRNdWMzVmlkMnhyYWk1c2FXNXJPamt3T0RFNllYVjBhRjloWlhNeE1qaGZiV1ExT21Ob1lXTm9ZVEl3TFdsbGRHWTZkR3h6TVM0eVgzUnBZMnRsZEY5aGRYUm9PbGt5VmxkU2JuQnZaV3BSTHo5dlltWnpjR0Z5WVcwOVdrZHNlbGt6Vm5wak1teDJZbTVOZFZsWVFuZGlSMVYxV1RJNWRDWndjbTkwYjNCaGNtRnRQVTFVWXpCT1ZGazJXak5HTm1KVWFGTmtXRXBoVkZkU05XSnNSbEZTTTA1T1V6QjBiVkl5YkhKV01GSXdWRlpTVDFadE1DWnlaVzFoY210elBWY3RiVGRvVDIxSWExWXphVzFKV0d0Mk5GUnVkbHBtYld4eE9IcFBhelZzWkVkYWMyRllaMmRtUTBKRFVXdE5KbWR5YjNWd1BWVXpRbXhhVjFSdWRscEliblUxZW01d05VaHRhVzlCSm5Wa2NIQnZjblE5TUNaMWIzUTlNQQpzc3I6Ly9jeTExY3pFdWMzVmlkMnhyYWk1c2FXNXJPamd3T0RjNllYVjBhRjloWlhNeE1qaGZiV1ExT21Ob1lXTm9ZVEl3TFdsbGRHWTZkR3h6TVM0eVgzUnBZMnRsZEY5aGRYUm9PbGt5VmxkU2JuQnZaV3BSTHo5dlltWnpjR0Z5WVcwOVdrZHNlbGt6Vm5wak1teDJZbTVOZFZsWVFuZGlSMVYxV1RJNWRDWndjbTkwYjNCaGNtRnRQVTFVWXpCT1ZGazJXak5HTm1KVWFGTmtXRXBoVkZkU05XSnNSbEZTTTA1T1V6QjBiVkl5YkhKV01GSXdWRlpTVDFadE1DWnlaVzFoY210elBWY3RiVGRvVDIxSWExWXphVzFKV0c1MmJ6ZHNiVGN3ZUU5ck5XeGtSMXB6WVZobloyWkRRa2xSYXpnbVozSnZkWEE5VlROQ2JGcFhWRzUyV2todWRUVjZibkExU0cxcGIwRW1kV1J3Y0c5eWREMHdKblZ2ZEQwdwpzc3I6Ly9jeTExY3pJdWMzVmlkMnhyYWk1c2FXNXJPamd3T0RjNllYVjBhRjloWlhNeE1qaGZiV1ExT21Ob1lXTm9ZVEl3TFdsbGRHWTZkR3h6TVM0eVgzUnBZMnRsZEY5aGRYUm9PbGt5VmxkU2JuQnZaV3BSTHo5dlltWnpjR0Z5WVcwOVdrZHNlbGt6Vm5wak1teDJZbTVOZFZsWVFuZGlSMVYxV1RJNWRDWndjbTkwYjNCaGNtRnRQVTFVWXpCT1ZGazJXak5HTm1KVWFGTmtXRXBoVkZkU05XSnNSbEZTTTA1T1V6QjBiVkl5YkhKV01GSXdWRlpTVDFadE1DWnlaVzFoY210elBWY3RiVGRvVDIxSWExWXphVzFKV0c1MmJ6ZHNiVGN3ZVU5ck5XeGtSMXB6WVZobloyWkRRa2xSYXpnbVozSnZkWEE5VlROQ2JGcFhWRzUyV2todWRUVjZibkExU0cxcGIwRW1kV1J3Y0c5eWREMHdKblZ2ZEQwdwpzc3I6Ly9jeTExY3pNdWMzVmlkMnhyYWk1c2FXNXJPamd3T0RjNllYVjBhRjloWlhNeE1qaGZiV1ExT21Ob1lXTm9ZVEl3TFdsbGRHWTZkR3h6TVM0eVgzUnBZMnRsZEY5aGRYUm9PbGt5VmxkU2JuQnZaV3BSTHo5dlltWnpjR0Z5WVcwOVdrZHNlbGt6Vm5wak1teDJZbTVOZFZsWVFuZGlSMVYxV1RJNWRDWndjbTkwYjNCaGNtRnRQVTFVWXpCT1ZGazJXak5HTm1KVWFGTmtXRXBoVkZkU05XSnNSbEZTTTA1T1V6QjBiVkl5YkhKV01GSXdWRlpTVDFadE1DWnlaVzFoY210elBWY3RiVGRvVDIxSWExWXphVzFKV0c1MmJ6ZHNiVGN3ZWs5ck5XeGtSMXB6WVZobloyWkRRa2xSYXpnbVozSnZkWEE5VlROQ2JGcFhWRzUyV2todWRUVjZibkExU0cxcGIwRW1kV1J3Y0c5eWREMHdKblZ2ZEQwdwpzc3I6Ly9jeTExY3pRdWMzVmlkMnhyYWk1c2FXNXJPamd3T0RjNllYVjBhRjloWlhNeE1qaGZiV1ExT21Ob1lXTm9ZVEl3TFdsbGRHWTZkR3h6TVM0eVgzUnBZMnRsZEY5aGRYUm9PbGt5VmxkU2JuQnZaV3BSTHo5dlltWnpjR0Z5WVcwOVdrZHNlbGt6Vm5wak1teDJZbTVOZFZsWVFuZGlSMVYxV1RJNWRDWndjbTkwYjNCaGNtRnRQVTFVWXpCT1ZGazJXak5HTm1KVWFGTmtXRXBoVkZkU05XSnNSbEZTTTA1T1V6QjBiVkl5YkhKV01GSXdWRlpTVDFadE1DWnlaVzFoY210elBWY3RiVGRvVDIxSWExWXphVzFKV0c1MmJ6ZHNiVGN3TUU5ck5XeGtSMXB6WVZobloyWkRRa2xSYXpnbVozSnZkWEE5VlROQ2JGcFhWRzUyV2todWRUVjZibkExU0cxcGIwRW1kV1J3Y0c5eWREMHdKblZ2ZEQwdwpzc3I6Ly9jeTExY3pVdWMzVmlkMnhyYWk1c2FXNXJPamd3T0RjNllYVjBhRjloWlhNeE1qaGZiV1ExT21Ob1lXTm9ZVEl3TFdsbGRHWTZkR3h6TVM0eVgzUnBZMnRsZEY5aGRYUm9PbGt5VmxkU2JuQnZaV3BSTHo5dlltWnpjR0Z5WVcwOVdrZHNlbGt6Vm5wak1teDJZbTVOZFZsWVFuZGlSMVYxV1RJNWRDWndjbTkwYjNCaGNtRnRQVTFVWXpCT1ZGazJXak5HTm1KVWFGTmtXRXBoVkZkU05XSnNSbEZTTTA1T1V6QjBiVkl5YkhKV01GSXdWRlpTVDFadE1DWnlaVzFoY210elBWY3RiVGRvVDIxSWExWXphVzFKV0c1MmJ6ZHNiVGN3TVU5ck5XeGtSMXB6WVZobloyWkRRa2xSYXpnbVozSnZkWEE5VlROQ2JGcFhWRzUyV2todWRUVjZibkExU0cxcGIwRW1kV1J3Y0c5eWREMHdKblZ2ZEQwdwpzc3I6Ly9jeTExY3pZdWMzVmlkMnhyYWk1c2FXNXJPamd3T0RjNllYVjBhRjloWlhNeE1qaGZiV1ExT21Ob1lXTm9ZVEl3TFdsbGRHWTZkR3h6TVM0eVgzUnBZMnRsZEY5aGRYUm9PbGt5VmxkU2JuQnZaV3BSTHo5dlltWnpjR0Z5WVcwOVdrZHNlbGt6Vm5wak1teDJZbTVOZFZsWVFuZGlSMVYxV1RJNWRDWndjbTkwYjNCaGNtRnRQVTFVWXpCT1ZGazJXak5HTm1KVWFGTmtXRXBoVkZkU05XSnNSbEZTTTA1T1V6QjBiVkl5YkhKV01GSXdWRlpTVDFadE1DWnlaVzFoY210elBWY3RiVGRvVDIxSWExWXphVzFKV0c1MmJ6ZHNiVGN3TWs5ck5XeGtSMXB6WVZobloyWkRRa2xSYXpnbVozSnZkWEE5VlROQ2JGcFhWRzUyV2todWRUVjZibkExU0cxcGIwRW1kV1J3Y0c5eWREMHdKblZ2ZEQwdwpzc3I6Ly9jeTFvYXpFdWMzVmlkMnhyYWk1c2FXNXJPamd3T0RVNllYVjBhRjloWlhNeE1qaGZiV1ExT21Ob1lXTm9ZVEl3TFdsbGRHWTZkR3h6TVM0eVgzUnBZMnRsZEY5aGRYUm9PbGt5VmxkU2JuQnZaV3BSTHo5dlltWnpjR0Z5WVcwOVdrZHNlbGt6Vm5wak1teDJZbTVOZFZsWVFuZGlSMVYxV1RJNWRDWndjbTkwYjNCaGNtRnRQVTFVWXpCT1ZGazJXak5HTm1KVWFGTmtXRXBoVkZkU05XSnNSbEZTTTA1T1V6QjBiVkl5YkhKV01GSXdWRlpTVDFadE1DWnlaVzFoY210elBWY3RiVGRvVDIxSWExWXphVzFKV0hCd2NHNXRkVXM0ZUU5ck5XeGtSMXB6WVZobloyWkRRa2xSYXpnbVozSnZkWEE5VlROQ2JGcFhWRzUyV2todWRUVjZibkExU0cxcGIwRW1kV1J3Y0c5eWREMHdKblZ2ZEQwdwpzc3I6Ly9jeTFvYXpJdWMzVmlkMnhyYWk1c2FXNXJPamd3T0RVNllYVjBhRjloWlhNeE1qaGZiV1ExT21Ob1lXTm9ZVEl3TFdsbGRHWTZkR3h6TVM0eVgzUnBZMnRsZEY5aGRYUm9PbGt5VmxkU2JuQnZaV3BSTHo5dlltWnpjR0Z5WVcwOVdrZHNlbGt6Vm5wak1teDJZbTVOZFZsWVFuZGlSMVYxV1RJNWRDWndjbTkwYjNCaGNtRnRQVTFVWXpCT1ZGazJXak5HTm1KVWFGTmtXRXBoVkZkU05XSnNSbEZTTTA1T1V6QjBiVkl5YkhKV01GSXdWRlpTVDFadE1DWnlaVzFoY210elBWY3RiVGRvVDIxSWExWXphVzFKV0hCd2NHNXRkVXM0ZVU5ck5XeGtSMXB6WVZobloyWkRRa2xSYXpnbVozSnZkWEE5VlROQ2JGcFhWRzUyV2todWRUVjZibkExU0cxcGIwRW1kV1J3Y0c5eWREMHdKblZ2ZEQwdwpzc3I6Ly9jeTFvYXpNdWMzVmlkMnhyYWk1c2FXNXJPamd3T0RVNllYVjBhRjloWlhNeE1qaGZiV1ExT21Ob1lXTm9ZVEl3TFdsbGRHWTZkR3h6TVM0eVgzUnBZMnRsZEY5aGRYUm9PbGt5VmxkU2JuQnZaV3BSTHo5dlltWnpjR0Z5WVcwOVdrZHNlbGt6Vm5wak1teDJZbTVOZFZsWVFuZGlSMVYxV1RJNWRDWndjbTkwYjNCaGNtRnRQVTFVWXpCT1ZGazJXak5HTm1KVWFGTmtXRXBoVkZkU05XSnNSbEZTTTA1T1V6QjBiVkl5YkhKV01GSXdWRlpTVDFadE1DWnlaVzFoY210elBWY3RiVGRvVDIxSWExWXphVzFKV0hCd2NHNXRkVXM0ZWs5ck5XeGtSMXB6WVZobloyWkRRa2xSYXpnbVozSnZkWEE5VlROQ2JGcFhWRzUyV2todWRUVjZibkExU0cxcGIwRW1kV1J3Y0c5eWREMHdKblZ2ZEQwdwpzc3I6Ly9jeTFvYXpRdWMzVmlkMnhyYWk1c2FXNXJPamd3T0RVNllYVjBhRjloWlhNeE1qaGZiV1ExT21Ob1lXTm9ZVEl3TFdsbGRHWTZkR3h6TVM0eVgzUnBZMnRsZEY5aGRYUm9PbGt5VmxkU2JuQnZaV3BSTHo5dlltWnpjR0Z5WVcwOVdrZHNlbGt6Vm5wak1teDJZbTVOZFZsWVFuZGlSMVYxV1RJNWRDWndjbTkwYjNCaGNtRnRQVTFVWXpCT1ZGazJXak5HTm1KVWFGTmtXRXBoVkZkU05XSnNSbEZTTTA1T1V6QjBiVkl5YkhKV01GSXdWRlpTVDFadE1DWnlaVzFoY210elBWY3RiVGRvVDIxSWExWXphVzFKV0hCd2NHNXRkVXM0TUU5ck5XeGtSMXB6WVZobloyWkRRa2xSYXpnbVozSnZkWEE5VlROQ2JGcFhWRzUyV2todWRUVjZibkExU0cxcGIwRW1kV1J3Y0c5eWREMHdKblZ2ZEQwdwpzc3I6Ly9jeTFvYXpVdWMzVmlkMnhyYWk1c2FXNXJPamd3T0RVNllYVjBhRjloWlhNeE1qaGZiV1ExT21Ob1lXTm9ZVEl3TFdsbGRHWTZkR3h6TVM0eVgzUnBZMnRsZEY5aGRYUm9PbGt5VmxkU2JuQnZaV3BSTHo5dlltWnpjR0Z5WVcwOVdrZHNlbGt6Vm5wak1teDJZbTVOZFZsWVFuZGlSMVYxV1RJNWRDWndjbTkwYjNCaGNtRnRQVTFVWXpCT1ZGazJXak5HTm1KVWFGTmtXRXBoVkZkU05XSnNSbEZTTTA1T1V6QjBiVkl5YkhKV01GSXdWRlpTVDFadE1DWnlaVzFoY210elBWY3RiVGRvVDIxSWExWXphVzFKV0hCd2NHNXRkVXM0TVU5ck5XeGtSMXB6WVZobloyWkRRa2xSYXpnbVozSnZkWEE5VlROQ2JGcFhWRzUyV2todWRUVjZibkExU0cxcGIwRW1kV1J3Y0c5eWREMHdKblZ2ZEQwdwpzc3I6Ly9jeTFvYXpZdWMzVmlkMnhyYWk1c2FXNXJPamd3T0RVNllYVjBhRjloWlhNeE1qaGZiV1ExT21Ob1lXTm9ZVEl3TFdsbGRHWTZkR3h6TVM0eVgzUnBZMnRsZEY5aGRYUm9PbGt5VmxkU2JuQnZaV3BSTHo5dlltWnpjR0Z5WVcwOVdrZHNlbGt6Vm5wak1teDJZbTVOZFZsWVFuZGlSMVYxV1RJNWRDWndjbTkwYjNCaGNtRnRQVTFVWXpCT1ZGazJXak5HTm1KVWFGTmtXRXBoVkZkU05XSnNSbEZTTTA1T1V6QjBiVkl5YkhKV01GSXdWRlpTVDFadE1DWnlaVzFoY210elBWY3RiVGRvVDIxSWExWXphVzFKV0hCd2NHNXRkVXM0TWs5ck5XeGtSMXB6WVZobloyWkRRa2xSYXpnbVozSnZkWEE5VlROQ2JGcFhWRzUyV2todWRUVjZibkExU0cxcGIwRW1kV1J3Y0c5eWREMHdKblZ2ZEQwdwpzc3I6Ly9jeTEwZHpFdWMzVmlkMnhyYWk1c2FXNXJPamd3T0RnNllYVjBhRjloWlhNeE1qaGZiV1ExT21Ob1lXTm9ZVEl3TFdsbGRHWTZkR3h6TVM0eVgzUnBZMnRsZEY5aGRYUm9PbGt5VmxkU2JuQnZaV3BSTHo5dlltWnpjR0Z5WVcwOVdrZHNlbGt6Vm5wak1teDJZbTVOZFZsWVFuZGlSMVYxV1RJNWRDWndjbTkwYjNCaGNtRnRQVTFVWXpCT1ZGazJXak5HTm1KVWFGTmtXRXBoVkZkU05XSnNSbEZTTTA1T1V6QjBiVkl5YkhKV01GSXdWRlpTVDFadE1DWnlaVzFoY210elBWY3RiVGRvVDIxSWExWXphVzFKV0d4cU4wUnRkV0kwZUU5ck5XeGtSMXB6WVZobloyWkRSR3hwY1dwdWJFeDJibXh4T0NabmNtOTFjRDFWTTBKc1dsZFViblphU0c1MU5YcHVjRFZJYldsdlFTWjFaSEJ3YjNKMFBUQW1kVzkwUFRBCnNzcjovL2N5MTBkekl1YzNWaWQyeHJhaTVzYVc1ck9qZ3dPRGc2WVhWMGFGOWhaWE14TWpoZmJXUTFPbU5vWVdOb1lUSXdMV2xsZEdZNmRHeHpNUzR5WDNScFkydGxkRjloZFhSb09sa3lWbGRTYm5CdlpXcFJMejl2WW1aemNHRnlZVzA5V2tkc2Vsa3pWbnBqTW14MlltNU5kVmxZUW5kaVIxVjFXVEk1ZENad2NtOTBiM0JoY21GdFBVMVVZekJPVkZrMldqTkdObUpVYUZOa1dFcGhWRmRTTldKc1JsRlNNMDVPVXpCMGJWSXliSEpXTUZJd1ZGWlNUMVp0TUNaeVpXMWhjbXR6UFZjdGJUZG9UMjFJYTFZemFXMUpXR3hxTjBSdGRXSTBlVTlyTld4a1IxcHpZVmhuWjJaRFJHeHBjV3B1YkV4MmJteHhPQ1puY205MWNEMVZNMEpzV2xkVWJuWmFTRzUxTlhwdWNEVkliV2x2UVNaMVpIQndiM0owUFRBbWRXOTBQVEEKc3NyOi8vY3kxMGR6TXVjM1ZpZDJ4cmFpNXNhVzVyT2pnd09EZzZZWFYwYUY5aFpYTXhNamhmYldRMU9tTm9ZV05vWVRJd0xXbGxkR1k2ZEd4ek1TNHlYM1JwWTJ0bGRGOWhkWFJvT2xreVZsZFNibkJ2WldwUkx6OXZZbVp6Y0dGeVlXMDlXa2RzZWxrelZucGpNbXgyWW01TmRWbFlRbmRpUjFWMVdUSTVkQ1p3Y205MGIzQmhjbUZ0UFUxVVl6Qk9WRmsyV2pOR05tSlVhRk5rV0VwaFZGZFNOV0pzUmxGU00wNU9VekIwYlZJeWJISldNRkl3VkZaU1QxWnRNQ1p5WlcxaGNtdHpQVmN0YlRkb1QyMUlhMVl6YVcxSldHeHFOMFJ0ZFdJMGVrOXJOV3hrUjFwellWaG5aMlpEUkd4cGNXcHViRXgyYm14eE9DWm5jbTkxY0QxVk0wSnNXbGRVYm5aYVNHNTFOWHB1Y0RWSWJXbHZRU1oxWkhCd2IzSjBQVEFtZFc5MFBUQQpzc3I6Ly9jeTF6WjNBeExuTjFZbmRzYTJvdWJHbHVhem80TURjM09tRjFkR2hmWVdWek1USTRYMjFrTlRwamFHRmphR0V5TUMxcFpYUm1PblJzY3pFdU1sOTBhV05yWlhSZllYVjBhRHBaTWxaWFVtNXdiMlZxVVM4X2IySm1jM0JoY21GdFBWcEhiSHBaTTFaNll6SnNkbUp1VFhWWldFSjNZa2RWZFZreU9YUW1jSEp2ZEc5d1lYSmhiVDFOVkdNd1RsUlpObG96UmpaaVZHaFRaRmhLWVZSWFVqVmliRVpSVWpOT1RsTXdkRzFTTW14eVZqQlNNRlJXVWs5V2JUQW1jbVZ0WVhKcmN6MVhMVzAzYUU5dFNHdFdNMmx0U1ZodGJISkViR2x4Ukd4dVlVVjRUMnMxYkdSSFduTmhXR2RuWmtOQ1VXTnRiSFJhVTBKWFlWZFNiR0ozSm1keWIzVndQVlV6UW14YVYxUnVkbHBJYm5VMWVtNXdOVWh0YVc5QkpuVmtjSEJ2Y25ROU1DWjFiM1E5TUEKc3NyOi8vY3kxelozQXlMbk4xWW5kc2Eyb3ViR2x1YXpvNE1EYzNPbUYxZEdoZllXVnpNVEk0WDIxa05UcGphR0ZqYUdFeU1DMXBaWFJtT25Sc2N6RXVNbDkwYVdOclpYUmZZWFYwYURwWk1sWlhVbTV3YjJWcVVTOF9iMkptYzNCaGNtRnRQVnBIYkhwWk0xWjZZekpzZG1KdVRYVlpXRUozWWtkVmRWa3lPWFFtY0hKdmRHOXdZWEpoYlQxTlZHTXdUbFJaTmxvelJqWmlWR2hUWkZoS1lWUlhValZpYkVaUlVqTk9UbE13ZEcxU01teHlWakJTTUZSV1VrOVdiVEFtY21WdFlYSnJjejFYTFcwM2FFOXRTR3RXTTJsdFNWaHRiSEpFYkdseFJHeHVZVVY1VDJzMWJHUkhXbk5oV0dkblprTkNVV050YkhSYVUwSlhZVmRTYkdKM0ptZHliM1Z3UFZVelFteGFWMVJ1ZGxwSWJuVTFlbTV3TlVodGFXOUJKblZrY0hCdmNuUTlNQ1oxYjNROU1BCnNzcjovL2N5MXpaM0F6TG5OMVluZHNhMm91YkdsdWF6bzRNRGMzT21GMWRHaGZZV1Z6TVRJNFgyMWtOVHBqYUdGamFHRXlNQzFwWlhSbU9uUnNjekV1TWw5MGFXTnJaWFJmWVhWMGFEcFpNbFpYVW01d2IyVnFVUzhfYjJKbWMzQmhjbUZ0UFZwSGJIcFpNMVo2WXpKc2RtSnVUWFZaV0VKM1lrZFZkVmt5T1hRbWNISnZkRzl3WVhKaGJUMU5WR013VGxSWk5sb3pSalppVkdoVFpGaEtZVlJYVWpWaWJFWlJVak5PVGxNd2RHMVNNbXh5VmpCU01GUldVazlXYlRBbWNtVnRZWEpyY3oxWExXMDNhRTl0U0d0V00ybHRTVmh0YkhKRWJHbHhSR3h1WVVWNlQyczFiR1JIV25OaFdHZG5aa05DVVdOdGJIUmFVMEpYWVZkU2JHSjNKbWR5YjNWd1BWVXpRbXhhVjFSdWRscEliblUxZW01d05VaHRhVzlCSm5Wa2NIQnZjblE5TUNaMWIzUTlNQQpzc3I6Ly9jeTExYXpFdWMzVmlkMnhyYWk1c2FXNXJPamd3T0RrNllYVjBhRjloWlhNeE1qaGZiV1ExT21Ob1lXTm9ZVEl3TFdsbGRHWTZkR3h6TVM0eVgzUnBZMnRsZEY5aGRYUm9PbGt5VmxkU2JuQnZaV3BSTHo5dlltWnpjR0Z5WVcwOVdrZHNlbGt6Vm5wak1teDJZbTVOZFZsWVFuZGlSMVYxV1RJNWRDWndjbTkwYjNCaGNtRnRQVTFVWXpCT1ZGazJXak5HTm1KVWFGTmtXRXBoVkZkU05XSnNSbEZTTTA1T1V6QjBiVkl5YkhKV01GSXdWRlpTVDFadE1DWnlaVzFoY210elBWY3RiVGRvVDIxSWExWXphVzFKV0c5cE4waHNiVGN3ZUU5cFFrOWFXRkp0WWtkc05FbElkMmRSYTBwRUptZHliM1Z3UFZVelFteGFWMVJ1ZGxwSWJuVTFlbTV3TlVodGFXOUJKblZrY0hCdmNuUTlNQ1oxYjNROU1BCnNzcjovL2NuVXhMbk4xWW5kc2Eyb3ViR2x1YXpvM01EZ3hPbUYxZEdoZllXVnpNVEk0WDIxa05UcGphR0ZqYUdFeU1DMXBaWFJtT25Sc2N6RXVNbDkwYVdOclpYUmZZWFYwYURwWk1sWlhVbTV3YjJWcVVTOF9iMkptYzNCaGNtRnRQVnBIYkhwWk0xWjZZekpzZG1KdVRYVlpXRUozWWtkVmRWa3lPWFFtY0hKdmRHOXdZWEpoYlQxTlZHTXdUbFJaTmxvelJqWmlWR2hUWkZoS1lWUlhValZpYkVaUlVqTk9UbE13ZEcxU01teHlWakJTTUZSV1VrOVdiVEFtY21WdFlYSnJjejFYTFcxa2EzVnRWRzVHTTJ0Mk5GUnVkbHBtYld4eE9IaFBkVk0wYVdWbE9XdGxiWEp0VDIxQmJuY21aM0p2ZFhBOVZUTkNiRnBYVkc1MldraHVkVFY2Ym5BMVNHMXBiMEVtZFdSd2NHOXlkRDB3Sm5WdmREMHcKc3NyOi8vY25VeUxuTjFZbmRzYTJvdWJHbHVhem8zTURneE9tRjFkR2hmWVdWek1USTRYMjFrTlRwamFHRmphR0V5TUMxcFpYUm1PblJzY3pFdU1sOTBhV05yWlhSZllYVjBhRHBaTWxaWFVtNXdiMlZxVVM4X2IySm1jM0JoY21GdFBWcEhiSHBaTTFaNll6SnNkbUp1VFhWWldFSjNZa2RWZFZreU9YUW1jSEp2ZEc5d1lYSmhiVDFOVkdNd1RsUlpObG96UmpaaVZHaFRaRmhLWVZSWFVqVmliRVpSVWpOT1RsTXdkRzFTTW14eVZqQlNNRlJXVWs5V2JUQW1jbVZ0WVhKcmN6MVhMVzFrYTNWdFZHNUdNMnQyTkZSdWRscG1iV3h4T0hsUGRWTTBhV1ZsT1d0bGJYSnRUMjFCYm5jbVozSnZkWEE5VlROQ2JGcFhWRzUyV2todWRUVjZibkExU0cxcGIwRW1kV1J3Y0c5eWREMHdKblZ2ZEQwdwpzc3I6Ly9jblV6TG5OMVluZHNhMm91YkdsdWF6bzNNRGd4T21GMWRHaGZZV1Z6TVRJNFgyMWtOVHBqYUdGamFHRXlNQzFwWlhSbU9uUnNjekV1TWw5MGFXTnJaWFJmWVhWMGFEcFpNbFpYVW01d2IyVnFVUzhfYjJKbWMzQmhjbUZ0UFZwSGJIcFpNMVo2WXpKc2RtSnVUWFZaV0VKM1lrZFZkVmt5T1hRbWNISnZkRzl3WVhKaGJUMU5WR013VGxSWk5sb3pSalppVkdoVFpGaEtZVlJYVWpWaWJFWlJVak5PVGxNd2RHMVNNbXh5VmpCU01GUldVazlXYlRBbWNtVnRZWEpyY3oxWExXMWthM1Z0Vkc1R00ydDJORlJ1ZGxwbWJXeHhPSHBQZFZNMGFXVmxPV3RsYlhKdFQyMUJibmNtWjNKdmRYQTlWVE5DYkZwWFZHNTJXa2h1ZFRWNmJuQTFTRzFwYjBFbWRXUndjRzl5ZEQwd0puVnZkRDB3CnNzcjovL2NuVTBMbk4xWW5kc2Eyb3ViR2x1YXpvM01EZ3hPbUYxZEdoZllXVnpNVEk0WDIxa05UcGphR0ZqYUdFeU1DMXBaWFJtT25Sc2N6RXVNbDkwYVdOclpYUmZZWFYwYURwWk1sWlhVbTV3YjJWcVVTOF9iMkptYzNCaGNtRnRQVnBIYkhwWk0xWjZZekpzZG1KdVRYVlpXRUozWWtkVmRWa3lPWFFtY0hKdmRHOXdZWEpoYlQxTlZHTXdUbFJaTmxvelJqWmlWR2hUWkZoS1lWUlhValZpYkVaUlVqTk9UbE13ZEcxU01teHlWakJTTUZSV1VrOVdiVEFtY21WdFlYSnJjejFYTFcxa2EzVnRWRzVHTTJ0Mk5GUnVkbHBtYld4eE9EQlBkVk0wYVdWbE9XdGxiWEp0VDIxQmJuY21aM0p2ZFhBOVZUTkNiRnBYVkc1MldraHVkVFY2Ym5BMVNHMXBiMEVtZFdSd2NHOXlkRDB3Sm5WdmREMHcKc3NyOi8vY25VMUxuTjFZbmRzYTJvdWJHbHVhem8zTURneE9tRjFkR2hmWVdWek1USTRYMjFrTlRwamFHRmphR0V5TUMxcFpYUm1PblJzY3pFdU1sOTBhV05yWlhSZllYVjBhRHBaTWxaWFVtNXdiMlZxVVM4X2IySm1jM0JoY21GdFBWcEhiSHBaTTFaNll6SnNkbUp1VFhWWldFSjNZa2RWZFZreU9YUW1jSEp2ZEc5d1lYSmhiVDFOVkdNd1RsUlpObG96UmpaaVZHaFRaRmhLWVZSWFVqVmliRVpSVWpOT1RsTXdkRzFTTW14eVZqQlNNRlJXVWs5V2JUQW1jbVZ0WVhKcmN6MVhMVzFrYTNWdFZHNUdNMnQyTkZSdWRscG1iV3h4T0RGUGRWTTBhV1ZsT1d0bGJYSnRUMjFCYm5jbVozSnZkWEE5VlROQ2JGcFhWRzUyV2todWRUVjZibkExU0cxcGIwRW1kV1J3Y0c5eWREMHdKblZ2ZEQwdwpzc3I6Ly9jblUyTG5OMVluZHNhMm91YkdsdWF6bzNNRGd4T21GMWRHaGZZV1Z6TVRJNFgyMWtOVHBqYUdGamFHRXlNQzFwWlhSbU9uUnNjekV1TWw5MGFXTnJaWFJmWVhWMGFEcFpNbFpYVW01d2IyVnFVUzhfYjJKbWMzQmhjbUZ0UFZwSGJIcFpNMVo2WXpKc2RtSnVUWFZaV0VKM1lrZFZkVmt5T1hRbWNISnZkRzl3WVhKaGJUMU5WR013VGxSWk5sb3pSalppVkdoVFpGaEtZVlJYVWpWaWJFWlJVak5PVGxNd2RHMVNNbXh5VmpCU01GUldVazlXYlRBbWNtVnRZWEpyY3oxWExXMWthM1Z0Vkc1R00ydDJORlJ1ZGxwbWJXeHhPREpQZFZNMGFXVmxPV3RsYlhKdFQyMUJibmNtWjNKdmRYQTlWVE5DYkZwWFZHNTJXa2h1ZFRWNmJuQTFTRzFwYjBFbWRXUndjRzl5ZEQwd0puVnZkRDB3CnNzcjovL2FuQXhMbk4xWW5kc2Eyb3ViR2x1YXpvM01EZ3pPbUYxZEdoZllXVnpNVEk0WDIxa05UcGphR0ZqYUdFeU1DMXBaWFJtT25Sc2N6RXVNbDkwYVdOclpYUmZZWFYwYURwWk1sWlhVbTV3YjJWcVVTOF9iMkptYzNCaGNtRnRQVnBIYkhwWk0xWjZZekpzZG1KdVRYVlpXRUozWWtkVmRWa3lPWFFtY0hKdmRHOXdZWEpoYlQxTlZHTXdUbFJaTmxvelJqWmlWR2hUWkZoS1lWUlhValZpYkVaUlVqTk9UbE13ZEcxU01teHlWakJTTUZSV1VrOVdiVEFtY21WdFlYSnJjejFYTFcxa2EzVnRWRzVHTTIxc05saHRia3QzZURjM2VXRTFUR2xLTlRjeVVqWmhkVmsyV1VObUptZHliM1Z3UFZVelFteGFWMVJ1ZGxwSWJuVTFlbTV3TlVodGFXOUJKblZrY0hCdmNuUTlNQ1oxYjNROU1BCnNzcjovL2FuQXlMbk4xWW5kc2Eyb3ViR2x1YXpvM01EZ3pPbUYxZEdoZllXVnpNVEk0WDIxa05UcGphR0ZqYUdFeU1DMXBaWFJtT25Sc2N6RXVNbDkwYVdOclpYUmZZWFYwYURwWk1sWlhVbTV3YjJWcVVTOF9iMkptYzNCaGNtRnRQVnBIYkhwWk0xWjZZekpzZG1KdVRYVlpXRUozWWtkVmRWa3lPWFFtY0hKdmRHOXdZWEpoYlQxTlZHTXdUbFJaTmxvelJqWmlWR2hUWkZoS1lWUlhValZpYkVaUlVqTk9UbE13ZEcxU01teHlWakJTTUZSV1VrOVdiVEFtY21WdFlYSnJjejFYTFcxa2EzVnRWRzVHTTIxc05saHRia3QzZVRjM2VXRTFUR2xLTlRjeVVqWmhkVmsyV1VObUptZHliM1Z3UFZVelFteGFWMVJ1ZGxwSWJuVTFlbTV3TlVodGFXOUJKblZrY0hCdmNuUTlNQ1oxYjNROU1BCnNzcjovL2FuQXpMbk4xWW5kc2Eyb3ViR2x1YXpvM01EZ3pPbUYxZEdoZllXVnpNVEk0WDIxa05UcGphR0ZqYUdFeU1DMXBaWFJtT25Sc2N6RXVNbDkwYVdOclpYUmZZWFYwYURwWk1sWlhVbTV3YjJWcVVTOF9iMkptYzNCaGNtRnRQVnBIYkhwWk0xWjZZekpzZG1KdVRYVlpXRUozWWtkVmRWa3lPWFFtY0hKdmRHOXdZWEpoYlQxTlZHTXdUbFJaTmxvelJqWmlWR2hUWkZoS1lWUlhValZpYkVaUlVqTk9UbE13ZEcxU01teHlWakJTTUZSV1VrOVdiVEFtY21WdFlYSnJjejFYTFcxa2EzVnRWRzVHTTIxc05saHRia3QzZWpjM2VXRTFUR2xLTlRjeVVqWmhkVmsyV1VObUptZHliM1Z3UFZVelFteGFWMVJ1ZGxwSWJuVTFlbTV3TlVodGFXOUJKblZrY0hCdmNuUTlNQ1oxYjNROU1BCnNzcjovL2FuQTBMbk4xWW5kc2Eyb3ViR2x1YXpvM01EZ3pPbUYxZEdoZllXVnpNVEk0WDIxa05UcGphR0ZqYUdFeU1DMXBaWFJtT25Sc2N6RXVNbDkwYVdOclpYUmZZWFYwYURwWk1sWlhVbTV3YjJWcVVTOF9iMkptYzNCaGNtRnRQVnBIYkhwWk0xWjZZekpzZG1KdVRYVlpXRUozWWtkVmRWa3lPWFFtY0hKdmRHOXdZWEpoYlQxTlZHTXdUbFJaTmxvelJqWmlWR2hUWkZoS1lWUlhValZpYkVaUlVqTk9UbE13ZEcxU01teHlWakJTTUZSV1VrOVdiVEFtY21WdFlYSnJjejFYTFcxa2EzVnRWRzVHTTIxc05saHRia3QzTURjM2VXRTFUR2xLTlRjeVVqWmhkVmsyV1VObUptZHliM1Z3UFZVelFteGFWMVJ1ZGxwSWJuVTFlbTV3TlVodGFXOUJKblZrY0hCdmNuUTlNQ1oxYjNROU1BCnNzcjovL2FuQTFMbk4xWW5kc2Eyb3ViR2x1YXpvM01EZ3pPbUYxZEdoZllXVnpNVEk0WDIxa05UcGphR0ZqYUdFeU1DMXBaWFJtT25Sc2N6RXVNbDkwYVdOclpYUmZZWFYwYURwWk1sWlhVbTV3YjJWcVVTOF9iMkptYzNCaGNtRnRQVnBIYkhwWk0xWjZZekpzZG1KdVRYVlpXRUozWWtkVmRWa3lPWFFtY0hKdmRHOXdZWEpoYlQxTlZHTXdUbFJaTmxvelJqWmlWR2hUWkZoS1lWUlhValZpYkVaUlVqTk9UbE13ZEcxU01teHlWakJTTUZSV1VrOVdiVEFtY21WdFlYSnJjejFYTFcxa2EzVnRWRzVHTTIxc05saHRia3QzTVRjM2VXRTFUR2xLTlRjeVVqWmhkVmsyV1VObUptZHliM1Z3UFZVelFteGFWMVJ1ZGxwSWJuVTFlbTV3TlVodGFXOUJKblZrY0hCdmNuUTlNQ1oxYjNROU1BCnNzcjovL2FuQTJMbk4xWW5kc2Eyb3ViR2x1YXpvM01EZ3pPbUYxZEdoZllXVnpNVEk0WDIxa05UcGphR0ZqYUdFeU1DMXBaWFJtT25Sc2N6RXVNbDkwYVdOclpYUmZZWFYwYURwWk1sWlhVbTV3YjJWcVVTOF9iMkptYzNCaGNtRnRQVnBIYkhwWk0xWjZZekpzZG1KdVRYVlpXRUozWWtkVmRWa3lPWFFtY0hKdmRHOXdZWEpoYlQxTlZHTXdUbFJaTmxvelJqWmlWR2hUWkZoS1lWUlhValZpYkVaUlVqTk9UbE13ZEcxU01teHlWakJTTUZSV1VrOVdiVEFtY21WdFlYSnJjejFYTFcxa2EzVnRWRzVHTTIxc05saHRia3QzTWpjM2VXRTFUR2xLTlRjeVVqWmhkVmsyV1VObUptZHliM1Z3UFZVelFteGFWMVJ1ZGxwSWJuVTFlbTV3TlVodGFXOUJKblZrY0hCdmNuUTlNQ1oxYjNROU1BCnNzcjovL2FHc3hMbk4xWW5kc2Eyb3ViR2x1YXpvM01EZzFPbUYxZEdoZllXVnpNVEk0WDIxa05UcGphR0ZqYUdFeU1DMXBaWFJtT25Sc2N6RXVNbDkwYVdOclpYUmZZWFYwYURwWk1sWlhVbTV3YjJWcVVTOF9iMkptYzNCaGNtRnRQVnBIYkhwWk0xWjZZekpzZG1KdVRYVlpXRUozWWtkVmRWa3lPWFFtY0hKdmRHOXdZWEpoYlQxTlZHTXdUbFJaTmxvelJqWmlWR2hUWkZoS1lWUlhValZpYkVaUlVqTk9UbE13ZEcxU01teHlWakJTTUZSV1VrOVdiVEFtY21WdFlYSnJjejFYTFcxa2EzVnRWRzVHTTNCd2NHNXRkVXM0ZUU5MVV6UnBaV1U1YTJWdGNtMVBiVUZ1ZHlabmNtOTFjRDFWTTBKc1dsZFViblphU0c1MU5YcHVjRFZJYldsdlFTWjFaSEJ3YjNKMFBUQW1kVzkwUFRBCnNzcjovL2FHc3lMbk4xWW5kc2Eyb3ViR2x1YXpvM01EZzFPbUYxZEdoZllXVnpNVEk0WDIxa05UcGphR0ZqYUdFeU1DMXBaWFJtT25Sc2N6RXVNbDkwYVdOclpYUmZZWFYwYURwWk1sWlhVbTV3YjJWcVVTOF9iMkptYzNCaGNtRnRQVnBIYkhwWk0xWjZZekpzZG1KdVRYVlpXRUozWWtkVmRWa3lPWFFtY0hKdmRHOXdZWEpoYlQxTlZHTXdUbFJaTmxvelJqWmlWR2hUWkZoS1lWUlhValZpYkVaUlVqTk9UbE13ZEcxU01teHlWakJTTUZSV1VrOVdiVEFtY21WdFlYSnJjejFYTFcxa2EzVnRWRzVHTTNCd2NHNXRkVXM0ZVU5MVV6UnBaV1U1YTJWdGNtMVBiVUZ1ZHlabmNtOTFjRDFWTTBKc1dsZFViblphU0c1MU5YcHVjRFZJYldsdlFTWjFaSEJ3YjNKMFBUQW1kVzkwUFRBCnNzcjovL2FHc3pMbk4xWW5kc2Eyb3ViR2x1YXpvM01EZzFPbUYxZEdoZllXVnpNVEk0WDIxa05UcGphR0ZqYUdFeU1DMXBaWFJtT25Sc2N6RXVNbDkwYVdOclpYUmZZWFYwYURwWk1sWlhVbTV3YjJWcVVTOF9iMkptYzNCaGNtRnRQVnBIYkhwWk0xWjZZekpzZG1KdVRYVlpXRUozWWtkVmRWa3lPWFFtY0hKdmRHOXdZWEpoYlQxTlZHTXdUbFJaTmxvelJqWmlWR2hUWkZoS1lWUlhValZpYkVaUlVqTk9UbE13ZEcxU01teHlWakJTTUZSV1VrOVdiVEFtY21WdFlYSnJjejFYTFcxa2EzVnRWRzVHTTNCd2NHNXRkVXM0ZWs5MVV6UnBaV1U1YTJWdGNtMVBiVUZ1ZHlabmNtOTFjRDFWTTBKc1dsZFViblphU0c1MU5YcHVjRFZJYldsdlFTWjFaSEJ3YjNKMFBUQW1kVzkwUFRBCnNzcjovL2RYTXhMbk4xWW5kc2Eyb3ViR2x1YXpvM01EZzNPbUYxZEdoZllXVnpNVEk0WDIxa05UcGphR0ZqYUdFeU1DMXBaWFJtT25Sc2N6RXVNbDkwYVdOclpYUmZZWFYwYURwWk1sWlhVbTV3YjJWcVVTOF9iMkptYzNCaGNtRnRQVnBIYkhwWk0xWjZZekpzZG1KdVRYVlpXRUozWWtkVmRWa3lPWFFtY0hKdmRHOXdZWEpoYlQxTlZHTXdUbFJaTmxvelJqWmlWR2hUWkZoS1lWUlhValZpYkVaUlVqTk9UbE13ZEcxU01teHlWakJTTUZSV1VrOVdiVEFtY21WdFlYSnJjejFYTFcxa2EzVnRWRzVHTTI1MmJ6ZHNiVGN3ZUU5MVV6UnBaV1U1YTJWdGNtMVBiVUZ1ZHlabmNtOTFjRDFWTTBKc1dsZFViblphU0c1MU5YcHVjRFZJYldsdlFTWjFaSEJ3YjNKMFBUQW1kVzkwUFRBCnNzcjovL2RYTXlMbk4xWW5kc2Eyb3ViR2x1YXpvM01EZzNPbUYxZEdoZllXVnpNVEk0WDIxa05UcGphR0ZqYUdFeU1DMXBaWFJtT25Sc2N6RXVNbDkwYVdOclpYUmZZWFYwYURwWk1sWlhVbTV3YjJWcVVTOF9iMkptYzNCaGNtRnRQVnBIYkhwWk0xWjZZekpzZG1KdVRYVlpXRUozWWtkVmRWa3lPWFFtY0hKdmRHOXdZWEpoYlQxTlZHTXdUbFJaTmxvelJqWmlWR2hUWkZoS1lWUlhValZpYkVaUlVqTk9UbE13ZEcxU01teHlWakJTTUZSV1VrOVdiVEFtY21WdFlYSnJjejFYTFcxa2EzVnRWRzVHTTI1MmJ6ZHNiVGN3ZVU5MVV6UnBaV1U1YTJWdGNtMVBiVUZ1ZHlabmNtOTFjRDFWTTBKc1dsZFViblphU0c1MU5YcHVjRFZJYldsdlFTWjFaSEJ3YjNKMFBUQW1kVzkwUFRBCnNzcjovL2RYTXpMbk4xWW5kc2Eyb3ViR2x1YXpvM01EZzNPbUYxZEdoZllXVnpNVEk0WDIxa05UcGphR0ZqYUdFeU1DMXBaWFJtT25Sc2N6RXVNbDkwYVdOclpYUmZZWFYwYURwWk1sWlhVbTV3YjJWcVVTOF9iMkptYzNCaGNtRnRQVnBIYkhwWk0xWjZZekpzZG1KdVRYVlpXRUozWWtkVmRWa3lPWFFtY0hKdmRHOXdZWEpoYlQxTlZHTXdUbFJaTmxvelJqWmlWR2hUWkZoS1lWUlhValZpYkVaUlVqTk9UbE13ZEcxU01teHlWakJTTUZSV1VrOVdiVEFtY21WdFlYSnJjejFYTFcxa2EzVnRWRzVHTTI1MmJ6ZHNiVGN3ZWs5MVV6UnBaV1U1YTJWdGNtMVBiVUZ1ZHlabmNtOTFjRDFWTTBKc1dsZFViblphU0c1MU5YcHVjRFZJYldsdlFTWjFaSEJ3YjNKMFBUQW1kVzkwUFRBCnNzcjovL2RHVnpkRFF1YzNWaWQyeHJhaTVzYVc1ck9qY3dPRFU2WVhWMGFGOWhaWE14TWpoZmJXUTFPbU5vWVdOb1lUSXdMV2xsZEdZNmRHeHpNUzR5WDNScFkydGxkRjloZFhSb09sa3lWbGRTYm5CdlpXcFJMejl2WW1aemNHRnlZVzA5V2tkc2Vsa3pWbnBqTW14MlltNU5kVmxZUW5kaVIxVjFXVEk1ZENad2NtOTBiM0JoY21GdFBVMVVZekJPVkZrMldqTkdObUpVYUZOa1dFcGhWRmRTTldKc1JsRlNNMDVPVXpCMGJWSXliSEpXTUZJd1ZGWlNUMVp0TUNaeVpXMWhjbXR6UFZjdGJXUnJkVzFVYmtZemIzSTNabXhwTjE5cmRtSmZibXhMYW0xdVMzcHJkWEZtYkdzMFNHOTJZWHBzYWpWSWIzSTBWRzl5Y25Kc2JUY3piR2h2V0cxc1RGOXRjM0oyYld4eVJIQnNOM01tWjNKdmRYQTlWVE5DYkZwWFZHNTJXa2h1ZFRWNmJuQTFTRzFwYjBFbWRXUndjRzl5ZEQwd0puVnZkRDB3CnNzcjovL2RHVnpkREV1YzNWaWQyeHJhaTVzYVc1ck9qY3dPRFU2WVhWMGFGOWhaWE14TWpoZmJXUTFPbU5vWVdOb1lUSXdMV2xsZEdZNmRHeHpNUzR5WDNScFkydGxkRjloZFhSb09sa3lWbGRTYm5CdlpXcFJMejl2WW1aemNHRnlZVzA5V2tkc2Vsa3pWbnBqTW14MlltNU5kVmxZUW5kaVIxVjFXVEk1ZENad2NtOTBiM0JoY21GdFBVMVVZekJPVkZrMldqTkdObUpVYUZOa1dFcGhWRmRTTldKc1JsRlNNMDVPVXpCMGJWSXliSEpXTUZJd1ZGWlNUMVp0TUNaeVpXMWhjbXR6UFZjdGJXUnJkVzFVYmtZeE0yUXpZM1ZqTTBKc1dsZFNNMkpIZEhGTWJVNTJZbEVtWjNKdmRYQTlWVE5DYkZwWFZHNTJXa2h1ZFRWNmJuQTFTRzFwYjBFbWRXUndjRzl5ZEQwd0puVnZkRDB3CnNzcjovL2RHVnpkRE11YzNWaWQyeHJhaTVzYVc1ck9qY3dPRFU2WVhWMGFGOWhaWE14TWpoZmJXUTFPbU5vWVdOb1lUSXdMV2xsZEdZNmRHeHpNUzR5WDNScFkydGxkRjloZFhSb09sa3lWbGRTYm5CdlpXcFJMejl2WW1aemNHRnlZVzA5V2tkc2Vsa3pWbnBqTW14MlltNU5kVmxZUW5kaVIxVjFXVEk1ZENad2NtOTBiM0JoY21GdFBVMVVZekJPVkZrMldqTkdObUpVYUZOa1dFcGhWRmRTTldKc1JsRlNNMDVPVXpCMGJWSXliSEpXTUZJd1ZGWlNUMVp0TUNaeVpXMWhjbXR6UFZjdGJXUnJkVzFVYmtZemEzVTJVRzVyU1dKc2FsbG1iblZ4Wm01MU5qTnZkRXh1YkdseFFsZFBibkEyWkVjNWRrOUVWVEJQVVNabmNtOTFjRDFWTTBKc1dsZFViblphU0c1MU5YcHVjRFZJYldsdlFTWjFaSEJ3YjNKMFBUQW1kVzkwUFRB')
    result = temp.decode().split('\n')
    ess = []
    print(len(result))
    for i in result:
        res = decode_ssr(i, '测试备注', '测试组')
        ess.append(res)
    fsd = '\n'.join(ess)

    print(base64.b64encode(fsd.encode()).decode())
