# from recommendation_CF import CollaborativeFiltering
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
    user_similarity_cosine = np.zeros((user_size, user_size))
    user_similarity_jaccard = np.zeros((user_size, user_size))
    user_similarity_pearson = np.zeros((user_size, user_size))
    user_similarity_weight = np.random.random((user_size, user_size))
    b = np.mean(R_test[np.where(R_test != 0)])

    print("Initialize setting.....")
    print("User_size : %d, Item_size : %d" % (user_size, item_size))

    for user1 in range(user_size):
        for user2 in range(user_size):
            if np.count_nonzero(R_train[user1]) and np.count_nonzero(R_train[user2]):
                user_similarity_cosine[user1][user2] = 1 - scipy.spatial.distance.cosine(R_train[user1], R_train[user2])
                user_similarity_jaccard[user1][user2] = 1 - scipy.spatial.distance.jaccard(R_train[user1],
                                                                                           R_train[user2])
                try:
                    if not math.isnan(scipy.stats.pearsonr(R_train[user1], R_train[user2])[0]):
                        user_similarity_pearson[user1][user2] = scipy.stats.pearsonr(R_train[user1], R_train[user2])
                    else:
                        user_similarity_pearson[user1][user2] = 0
                except:
                    user_similarity_pearson[user1][user2] = 0

    print("Similarity calculated")

    ind = (R_train[:, R_train.nonzero()[1]])
    R_predicted_cosine = np.zeros([user_size, item_size])
    R_predicted_jaccard = np.zeros([user_size, item_size])
    R_predicted_pearson = np.zeros([user_size, item_size])

    sim_sum = np.zeros(user_size)
    sim_sum_j = np.zeros(user_size)
    sim_sum_p = np.zeros(user_size)

    for i in range(user_size):
        ind = np.argsort(user_similarity_cosine[:][i])[-100:]
        ind_j = np.argsort(user_similarity_jaccard[:][i][-100:])
        ind_p = np.argsort(user_similarity_pearson[:][i][-100:])
        for j in ind:
            for k in range(len(R_train[j])):
                if R_train[j][k] != 0:
                    R_predicted_cosine[i][k] += user_similarity_cosine[i][j] * (R_train-b)[j][k]
            # R_predicted_cosine[i] += user_similarity_cosine[i][j] * (R_train-b)[j]
            sim_sum[i] += np.absolute(user_similarity_cosine[i][j])

        for j in ind_j:
            for k in range(len(R_train[j])):
                if R_train[j][k] != 0:
                    R_predicted_jaccard[i][k] += user_similarity_jaccard[i][j] * (R_train-b)[j][k]
            # R_predicted_jaccard[i] += user_similarity_cosine[i][j] * (R_train-b)[j]
            sim_sum_j[i] += np.absolute(user_similarity_jaccard[i][j])

        for j in ind_p:
            for k in range(len(R_train[j])):
                if R_train[j][k] != 0:
                    R_predicted_pearson[i][k] += user_similarity_pearson[i][j] * (R_train-b)[j][k]
            # R_predicted_pearson[i] += user_similarity_cosine[i][j] * (R_train-b)[j]
            sim_sum_p[i] += np.absolute(user_similarity_pearson[i][j])

        if sim_sum[i] !=0:
            R_predicted_cosine[i] =  R_predicted_cosine[i] / sim_sum [i]
        R_predicted_cosine[i] += b

        if sim_sum_j[i] !=0:
            R_predicted_jaccard[i] =  R_predicted_jaccard[i] / sim_sum_j[i]
        R_predicted_jaccard[i] += b

        if sim_sum_p[i] != 0:
            R_predicted_pearson[i] = R_predicted_pearson[i] / sim_sum_p[i]
        R_predicted_pearson[i] += b


    # R_predicted_jaccard = np.dot(user_similarity_jaccard, (R_train-b*np.ones(user_size, item_size)))/np.sum(np.absolute(user_similarity_jaccard[ind])) + b
    # R_predicted_pearson = np.dot(user_similarity_pearson, (R_train-b*np.ones(user_size, item_size)))/np.sum(np.absolute(user_similarity_pearson[ind])) + b

    print("Rating predicted...")

    R_predicted_cosine = np.clip(R_predicted_cosine, 0, 5)
    R_predicted_jaccard = np.clip(R_predicted_jaccard, 0, 5)
    R_predicted_pearson = np.clip(R_predicted_pearson, 0, 5)

    print("Clip rating from 0 to 5")
    print("Calculating RMSE score")

    text_xi, text_yi = R_test.nonzero()

    cost_cosine = 0
    cost_jaccard = 0
    cost_pearson = 0

    for xi, yi in zip(text_xi, text_yi):
        cost_cosine += pow(R_test[xi, yi] - R_predicted_cosine[xi, yi], 2)
        cost_jaccard += pow(R_test[xi, yi] - R_predicted_jaccard[xi, yi], 2)
        cost_pearson += pow(R_test[xi, yi] - R_predicted_pearson[xi, yi], 2)

    RMSE_score_cosine = np.sqrt(cost_cosine) / len(text_xi)
    RMSE_score_jaccard = np.sqrt(cost_jaccard) / len(text_xi)
    RMSE_score_pearson = np.sqrt(cost_pearson) / len(text_xi)

    print ("Cosine similarity error : %.6f \n Jaccard_similarity_error : %.6f \n Pearson_similarity_error : %.6f" % (RMSE_score_cosine, RMSE_score_jaccard, RMSE_score_pearson))
    RMSE_score = []
    RMSE_score.append(RMSE_score_cosine)
    RMSE_score.append(RMSE_score_jaccard)
    RMSE_score.append(RMSE_score_pearson)

    np.savetxt("./result/CF_result_sim_cosine.csv", user_similarity_cosine, delimiter=",")
    np.savetxt("./result/CF_result_sim_jaccard.csv", user_similarity_jaccard, delimiter=",")
    np.savetxt("./result/CF_result_sim_pearson.csv", user_similarity_pearson, delimiter=",")
    np.savetxt("./result/CF_result_cosine.csv", R_predicted_cosine, delimiter=",")
    np.savetxt("./result/CF_result_jaccard.csv", R_predicted_jaccard, delimiter=",")
    np.savetxt("./result/CF_result_pearson.csv", R_predicted_pearson, delimiter=",")

    np.savetxt("CF_result.csv", RMSE_score, delimiter=",")

    print ("All result are saved.")

    # CF_model = CollaborativeFiltering(R_train, k=3, learning_rate = 0.01, epochs = 300, verbose = True)
    # cosine_result =CF_model.get_similarity_user()

    # print (cosine_result)

