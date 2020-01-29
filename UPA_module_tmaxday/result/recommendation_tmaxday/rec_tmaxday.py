from result.recommendation_tmaxday.recommendation_tmaxday import MatrixFactorization, MatrixFactorization_test
import numpy as np

slicing_param = 66667
epoch = 10


if __name__ == "__main__":
	# rating matrix
	# data = surprise.Dataset.load_builtin('ml-100k')
	# df = pd.DataFrame(data.raw_ratings, columns=["user", "item", "rate", "id"])
	# del df["id"]

	csv_data = np.loadtxt("/home/choikoal/Downloads/item_list-user_item_table_data.csv", delimiter=",", dtype=np.float32)
	print (csv_data)

	# Test error Table
	test_er = []

	for i in range(epoch):

		# # Shuffle Tuple
		# df.sample(frac=1).reset_index(drop=True)
		#
		# # splicing training data and test data by 2:1
		# print("Training epoch = %d *********************************" % (i+1))
		# df_train = copy.copy(df) # shallow copy
		# train_dummy = copy.copy(df)
		# train = train_dummy[0:slicing_param]
		# lst = list(train["rate"])
		# dummy = np.zeros([100000-slicing_param])
		# lst = np.hstack([lst, dummy])
		# df_train["rate"] = tuple(lst)
		#
		# # generating test data
		# df_test = copy.copy(df)
		# test_dummy = copy.copy(df)
		# test = test_dummy[slicing_param:]
		# lst = list(test["rate"])
		# dummy = np.zeros([slicing_param])
		# lst = np.hstack([dummy, lst])
		# df_test["rate"] = tuple(lst)
		#
		# # unstack
		# train_table = df_train.set_index(["user", "item"]).unstack()
		# test_table = df_test.set_index(["user", "item"]).unstack()
		#
		# # convert to numpy array
		# train_data_array = train_table.values
		# test_data_array = test_table.values
		# R_train = np.nan_to_num(train_data_array)
		R_train = csv_data
		# R_test = np.nan_to_num(test_data_array)
		R_test = csv_data

		# Train
		factorizer = MatrixFactorization(R_train, k=10, learning_rate=0.01, reg_param=0.01, epochs=600, verbose=True)
		factorizer.fit()
		factorizer.print_results()
		trained_R = factorizer.get_complete_matrix()


		# Test
		tester = MatrixFactorization_test(trained_R, R_test)
		tester.print_result()

		# Save RMSE result
		np.savetxt("./result/Training_result_tmaxday_ep%d.csv"%(i+1), trained_R, delimiter=",")

		errorrr = tester.test()
		test_er.append(errorrr)
	print ("Test errors *****************************************")
	for i in range(epoch):
		print ("Epoch%d : %.6f" % (i+1, test_er[i]))

	# Save Test Result
	np.savetxt("Training_result_tmaxday.csv", test_er, delimiter=",")
	d = {}
	sum = np.zeros([22, 3])

	for i in range(epoch):
		d["csv_data" + str(i + 1)] = np.loadtxt(
			"/home/choikoal/PycharmProjects/recommendation_01/result/Training_result_tmaxday_ep%d.csv" % (i + 1),
			delimiter=",", dtype=np.float32)
		sum += d["csv_data" + str(i + 1)]

	avg = sum / epoch
	np.savetxt("/home/choikoal/PycharmProjects/recommendation_01/Training_result_average_tmaxday.csv", avg,
			   delimiter=",")
