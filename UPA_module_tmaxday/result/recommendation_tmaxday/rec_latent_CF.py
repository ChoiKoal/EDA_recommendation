# from recommendation_CF import compute_cost
import numpy as np
import pandas as pd
import surprise
import copy
import math
import scipy.spatial
import scipy.stats
import random
from surprise.model_selection import KFold

slicing_param = 66667
epoch = 10

def compute_cost(R_trained, R_test):
    """
    :return: test error
    """
    xi, yi = R_test.nonzero()
    cost = 0
    for x, y in zip(xi, yi):
        cost += pow(R_test[x, y] - R_trained[x, y], 2)
    return np.sqrt(cost) / len(xi)

def gradient(error, i, j):
    """

    :param error:
    :param i: user index
    :param j: item index
    :return:
    """
    dw = np.sum()

if __name__ == "__main__":
    # rating matrix
    data = surprise.Dataset.load_builtin('ml-100k')

    df = pd.DataFrame(data.raw_ratings, columns=["user", "item", "rate", "id"])
    del df["id"]


    # Test error table
    test_er = []

    # Shuffle Tuple
    df.sample(frac=1).reset_index(drop=True)

    # splicing training data and test data by 2:1
    # print("Training epoch = %d *********************************" % (i + 1))
    df_train = copy.copy(df)  # shallow copy
    train_dummy = copy.copy(df)
    train = train_dummy[0:slicing_param]
    lst = list(train["rate"])
    dummy = np.zeros([100000 - slicing_param])
    lst = np.hstack([lst, dummy])
    df_train["rate"] = tuple(lst)

    # generating test data
    df_test = copy.copy(df)
    test_dummy = copy.copy(df)
    test = test_dummy[slicing_param:]
    lst = list(test["rate"])
    dummy = np.zeros([slicing_param])
    lst = np.hstack([dummy, lst])
    df_test["rate"] = tuple(lst)

    # unstack
    train_table = df_train.set_index(["user", "item"]).unstack()
    test_table = df_test.set_index(["user", "item"]).unstack()

    # convert to numpy array
    train_data_array = train_table.values
    test_data_array = test_table.values
    R_train = np.nan_to_num(train_data_array)
    R_test = np.nan_to_num(test_data_array)

    user_size, item_size = np.shape(R_train)
    R_predicted_weight = np.zeros([user_size, item_size])

    user_similarity_weight =  np.random.normal(size=(user_size, user_size))
    b = np.mean(R_test[np.where(R_test != 0)])
    print("Initialize setting.....")
    print("User_size : %d, Item_size : %d" % (user_size, item_size))

    for i in range(user_size):
        R_predicted_weight[i] = np.dot(user_similarity_weight[i], R_train)

    cost = compute_cost(R_predicted_weight, R_train)
    print (cost)



    print("Similarity calculated")

    ind = (R_train[:, R_train.nonzero()[1]])


    sim_sum = np.zeros(user_size)
    sim_sum_j = np.zeros(user_size)
    sim_sum_p = np.zeros(user_size)





    # R_predicted_jaccard = np.dot(user_similarity_jaccard, (R_train-b*np.ones(user_size, item_size)))/np.sum(np.absolute(user_similarity_jaccard[ind])) + b
    # R_predicted_pearson = np.dot(user_similarity_pearson, (R_train-b*np.ones(user_size, item_size)))/np.sum(np.absolute(user_similarity_pearson[ind])) + b

    print("Rating predicted...")



    print("Clip rating from 0 to 5")
    print("Calculating RMSE score")

    text_xi, text_yi = R_test.nonzero()

    cost_cosine = 0
    cost_jaccard = 0
    cost_pearson = 0





    print ("Cosine similarity error : %.6f \n Jaccard_similarity_error : %.6f \n Pearson_similarity_error : %.6f" % (RMSE_score_cosine, RMSE_score_jaccard, RMSE_score_pearson))
    RMSE_score = []
    # RMSE_score.append(RMSE_score_cosine)
    # RMSE_score.append(RMSE_score_jaccard)
    # RMSE_score.append(RMSE_score_pearson)

    # np.savetxt("./result/CF_result_sim_cosine.csv", user_similarity_cosine, delimiter=",")
    # np.savetxt("./result/CF_result_sim_jaccard.csv", user_similarity_jaccard, delimiter=",")
    # np.savetxt("./result/CF_result_sim_pearson.csv", user_similarity_pearson, delimiter=",")
    # np.savetxt("./result/CF_result_cosine.csv", R_predicted_cosine, delimiter=",")
    # np.savetxt("./result/CF_result_jaccard.csv", R_predicted_jaccard, delimiter=",")
    # np.savetxt("./result/CF_result_pearson.csv", R_predicted_pearson, delimiter=",")

    np.savetxt("CF_result.csv", RMSE_score, delimiter=",")

    print ("All result are saved.")

    # CF_model = CollaborativeFiltering(R_train, k=3, learning_rate = 0.01, epochs = 300, verbose = True)
    # cosine_result =CF_model.get_similarity_user()

    # print (cosine_result)



