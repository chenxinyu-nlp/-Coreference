import glob
import pandas as pd
# KBP_TRAIN_PATH = ".//data//kbp2015_train_nugget.csv"
# KBP_TEST_PATH_2015 = ".//data//kbp2015_test_nugget.csv"
# KBP_TEST_PATH_2016 = ".//data//kbp2016_test_nugget.csv"
# KBP_TEST_PATH_2017 = ".//data//kbp2017_test_nugget.csv"
'''
本代码获取用于喂入同指模型的数据集。
训练集涉及到的语料库是kbp2015,
测试集涉及到的语料库是kbp2015, kbp2016, kbp2017
'''
class EventPairsFeature:
    def __init__(self):
        self.event_sentence1 = []
        self.event_sentence2 = []
        self.event_sub_type1 = []
        self.event_sub_type2 = []
        self.sub_type_same = []
        self.event_type1 = []
        self.event_type2 = []
        self.type_same = []
        self.doc_id1 = []
        self.doc_id2 = []
        self.event_trigger1 = []
        self.event_trigger2 = []
        self.event_trigger_same = []
        self.mod1 = []
        self.mod2 = []
        self.mod_same = []
        self.event_id1 = []
        self.event_id2 = []
        self.label = []
        pass

def print_obj(obj):
    print(len(obj.event_sentence1))
    print(len(obj.event_sentence2))
    print(len(obj.event_trigger1))
    print(len(obj.event_trigger2))
    print(len(obj.doc_id1))
    print(len(obj.doc_id2))
    print(len(obj.type_same))
    print(len(obj.sub_type_same))
    print(len(obj.mod_same))
    print(len(obj.event_trigger_same))
    print(len(obj.label))

path_list = glob.glob("data/*")# 得到待处理文件的列表
print(path_list)
path_list = (path_list[:2])[::-1]
print(path_list)


# 处理csv文件,将里面的事件凑成事件对
def deal_file(file_path):
    epf = EventPairsFeature()
    df = pd.read_csv(file_path, engine='python', encoding='utf-8')# 读取.csv数据文件
    event_sub_type = list(df['SubType'].values)# 获取所有事件子类型
    event_type = list(df['Type'].values)# 获取所有事件类型
    doc_id = list(df['docID'].values)# 获取文档id
    event_id = list(df['eventID'].values)# 获取事件id，这是事件的唯一标识
    event_sentence = list(df['eventSen'].values)
    event_trigger = list(df['eventTrigger'].values)
    mod = list(df['mod'].values)
    doc_len = len(event_sentence)
    for i in range(0, doc_len):
        for j in range(i+1, doc_len):
            if str(event_id[i]) == str(event_id[j]) and str(doc_id[i]) == str(doc_id[j]):# 只在同文本内做同指
                epf.event_sentence1.append(str(event_sentence[i]))
                epf.event_sentence2.append(str(event_sentence[j]))
                epf.event_trigger1.append(event_trigger[i])
                epf.event_trigger2.append(event_trigger[j])
                epf.doc_id1.append(doc_id[i])
                epf.doc_id2.append(doc_id[j])
                # 事件类型是否一致的标记
                if str(event_type[i]) == str(event_type[j]):
                    epf.type_same.append(1)
                else:
                    epf.type_same.append(0)
                # 事件类型和子类型是否一致的标记
                if str(event_type[i]) == str(event_type[j]) and str(event_sub_type[i]) == str(event_sub_type[j]):
                    epf.sub_type_same.append(1)
                else:
                    epf.sub_type_same.append(0)
                # 事件时态是否一致的标记
                if str(mod[i]) == str(mod[j]):
                    epf.mod_same.append(1)
                else:
                    epf.mod_same.append(0)
                # 事件触发词是否一致的标记
                if str(event_trigger[i]) == str(event_trigger[j]):
                    epf.event_trigger_same.append(1)
                else:
                    epf.event_trigger_same.append(0)
                # 同指标签为1
                epf.label.append(1)

    for i in range(0, doc_len):
        for j in range(i+1, doc_len):
            if str(doc_id[i]) == str(doc_id[j]):# 只在同文本内做同指
                if str(event_id[i]) != str(event_id[j]):
                    epf.event_sentence1.append(str(event_sentence[i]))
                    epf.event_sentence2.append(str(event_sentence[j]))
                    epf.event_trigger1.append(event_trigger[i])
                    epf.event_trigger2.append(event_trigger[j])
                    epf.doc_id1.append(doc_id[i])
                    epf.doc_id2.append(doc_id[j])
                    # 事件类型是否一致的标记
                    if str(event_type[i]) == str(event_type[j]):
                        epf.type_same.append(1)
                    else:
                        epf.type_same.append(0)
                    # 事件类型和子类型是否一致的标记
                    if str(event_type[i]) == str(event_type[j]) and str(event_sub_type[i]) == str(event_sub_type[j]):
                        epf.sub_type_same.append(1)
                    else:
                        epf.sub_type_same.append(0)
                    # 事件时态是否一致的标记
                    if str(mod[i]) == str(mod[j]):
                        epf.mod_same.append(1)
                    else:
                        epf.mod_same.append(0)
                    # 事件触发词是否一致的标记
                    if str(event_trigger[i]) == str(event_trigger[j]):
                        epf.event_trigger_same.append(1)
                    else:
                        epf.event_trigger_same.append(0)
                    # 非同指标签为0
                    epf.label.append(0)
    return epf

if __name__ == '__main__':
    event_pairs_obj = []
    for path in path_list:
        event_pairs = deal_file(path)
        event_pairs_obj.append(event_pairs)
        print(path)
        print(event_pairs)

    print_obj(event_pairs_obj[0])
    print_obj(event_pairs_obj[1])

    count0_coref = 0
    count0_noncoref = 0
    for i in range(len(event_pairs_obj[0].label)):
        if event_pairs_obj[0].label[i] == 1:
            count0_coref += 1
        else:
            count0_noncoref += 1
    print(count0_coref)
    print(count0_noncoref)

    count1_coref = 0
    count1_noncoref = 0
    for i in range(len(event_pairs_obj[1].label)):
        if event_pairs_obj[1].label[i] == 1:
            count1_coref += 1
        else:
            count1_noncoref += 1

    print(count1_coref)
    print(count1_noncoref)