import requests
import re
from Crypto.Cipher import AES


def m3u8(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    }
    # requests得到m3u8文件内容
    content = requests.get(url, headers=header).text
    if "#EXTM3U" not in content:
        print("这不是一个m3u8的视频链接！")
        return False
    if "EXT-X-KEY" not in content:
        print("没有加密")
        return False

    # 使用re正则得到key和视频地址
    jiami = re.findall('#EXT-X-KEY:(.*)\n', content)
    key = re.findall('URI="(.*)"', jiami[0])
    vi = re.findall('IV=(.*)', jiami[0])[0]

    # 得到每一个ts视频链接
    tslist = re.findall('EXTINF:(.*),\n(.*)\n#', content)
    newlist = []
    for i in tslist:
        newlist.append(i[1])

    # 得到key的链接并请求得到加密的key值
    keyurl = key[0]
    keycontent = requests.get(keyurl, headers=header).content

    # 得到每一个完整视频的链接地址
    base_url = url.replace(url.split('/')[-1], '')
    print(base_url)
    tslisturl = []
    for i in newlist:
        tsurl = base_url + i
        tslisturl.append(tsurl)

    # 得到解密方法，这里要导入第三方库  pycrypto
    # 这里有一个问题，安装pycrypto成功后，导入from Crypto.Cipher import AES报错
    # 找到使用python环境的文件夹，在Lib文件夹下有一个 site-packages 文件夹，里面是我们环境安装的包。
    # 找到一个crypto文件夹，打开可以看到 Cipher文件夹，此时我们将 crypto文件夹改为 Crypto 即可使用了
    #     print(keycontent)
    cryptor = AES.new(keycontent, AES.MODE_CBC)

    # for循环获取视频文件
    for i in tslisturl:
        res = requests.get(i, header)
        # 使用解密方法解密得到的视频文件
        cont = cryptor.decrypt(res.content)
        # 以追加的形式保存为mp4文件
        with open('xx.mp4', 'ab+') as f:
            f.write(cont)
    return True


if __name__ == '__main__':
    url = "http://...........m3u8"
    pd = m3u8(url)
    if pd:
        print('视频下载完成！')
