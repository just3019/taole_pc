import jieba as jieba

text = "Apple 苹果 iphone Xs Max 移动联通电信4G手机 深空灰 256GB 【全新原封 国行正品 全国联保 京东物流 快捷安全 抢购苹果XS 送无线充+游戏辅助按键+壳+膜+指环扣】抢购苹果XR"

seg_list = jieba.cut(text, cut_all=True)
print(",".join(seg_list))  # 全模式

seg_list = jieba.cut(text, cut_all=False)
print(",".join(seg_list))  # 精确模式

seg_list = jieba.cut(text)  # 默认是精确模式
print(",".join(seg_list))

seg_list = jieba.cut_for_search(text)
print(",".join(seg_list))

