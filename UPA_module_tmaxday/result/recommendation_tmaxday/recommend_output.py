import numpy as np

# print("올해 월별 손익")
# print("올해 본부별 목표치 대비 매출")
# print("연도별 목표치 대비 매출")
avg = np.loadtxt("/home/choikoal/PycharmProjects/recommendation_01/Training_result_average_tmaxday.csv", delimiter=",", dtype=np.float32)
avg = np.sum(avg, axis=1)
ind = np.argsort(avg.T)[-3:]
output = np.loadtxt("/home/choikoal/PycharmProjects/recommendation_01/respsentence.csv", delimiter=",", dtype=str)
recommend = []
for index in range(len(ind)):
    recommend.append(output[ind[index]])
    print(output[ind[index]])
