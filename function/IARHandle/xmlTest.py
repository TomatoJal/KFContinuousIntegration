from lxml import etree


test = etree.parse('E:\\OnePiece\\Project\\0007.KFM\\Cetus_02_KF13A009M1\\IAR\\app2.ewp', etree.HTMLParser())
config = test.xpath(r'//configuration/name')[0]
config = config.xpath('..')[0]
print(config.xpath(r'./settings/data/option[name="ExePath"]/state/text()'))
