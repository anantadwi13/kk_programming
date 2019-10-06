import csv
from pprint import pprint
import math


def load_data_set(filename, k_fold=5):
    groups = []
    with open(filename, 'rt') as csvfile:
        dataset = csv.reader((line.replace('    ', ' ').replace('   ', ' ').replace('  ', ' ').replace(' ', ',')
                              for line in csvfile))
        dataset_list = list(dataset)
        i = 0
        max_item = math.ceil(len(dataset_list)/k_fold)
        for line in dataset_list:
            if i//max_item > len(groups)-1:
                groups.insert(i//max_item, [])
            instance = []
            for attrib in line:
                try:
                    instance.append(float(attrib))
                except:
                    instance.append(attrib)
            groups[i//max_item].append(instance)
            i += 1
        return groups


def euclidean_distance(data1, data2):
    distance = 0
    length = len(data1) if len(data1) < len(data2) else len(data2)
    for x in range(length):
        distance += pow(data1[x] - data2[x], 2)
    return math.sqrt(distance)


def manhattan_distance(data1, data2):
    distance = 0
    length = len(data1) if len(data1) < len(data2) else len(data2)
    for x in range(length):
        distance += abs(data1[x] - data2[x])
    return distance


def cosine_similarity_distance(data1, data2):
    distance = 0
    length = len(data1) if len(data1) < len(data2) else len(data2)
    for x in range(length):
        distance += abs(data1[x] - data2[x])
    return distance


def get_neighbors(data_trains, data_test, k, distance_algo=1):
    d_test = data_test.copy()
    d_test.pop(0)
    d_test.pop(-1)
    #print([type(y) for y in d_test])

    distances = []
    neighbors = []
    for x in range(len(data_trains)):
        d_train = data_trains[x].copy()
        d_train.pop(0)
        d_train.pop(-1)
        #print([type(y) for y in d_train])

        if distance_algo == 2:
            distance = manhattan_distance(d_train, d_test)
        elif distance_algo == 3:
            distance = cosine_similarity_distance(d_train, d_test)
        else:
            distance = euclidean_distance(d_train, d_test)
        distances.append((data_trains[x], distance))
    distances.sort(key=lambda tup: tup[1])

    for x in range(k):
        neighbors.append(distances[x])

    return neighbors


def get_majority_vote(data_neighbors):
    votes = {}
    for item in data_neighbors:
        class_vote = item[0][-1]
        if class_vote in votes:
            votes[class_vote] += 1
        else:
            votes[class_vote] = 1

    sorted_votes = sorted(votes.items(), key=lambda tup: tup[1], reverse=True)
    return sorted_votes[0][0]


if __name__ == '__main__':
    k = 10
    k_fold = 10
    distance = 1
    # 1 euclidean, 2 manhattan, 3 cosine similarity, default euclidean

    dataset = load_data_set('yeast.data', k_fold)

    total_accuracy = 0
    for id_group in range(k_fold):
        temp_data_trains = dataset.copy()
        data_tests = temp_data_trains.pop(id_group)
        data_trains = []
        for group in temp_data_trains:
            for item in group:
                data_trains.append(item)

        if id_group == 0:
            print('Total data trains : ' + str(len(data_trains)))
            print('Total data tests : ' + str(len(data_tests)))
            print('Total data tests : 1:' + str(math.ceil(len(data_trains)/len(data_tests))))

        correct = 0
        for data_test in data_tests:
            neighbors = get_neighbors(data_trains, data_test, k, distance)
            class_test = data_test[-1]
            class_predict = get_majority_vote(neighbors)
            # print(neighbors)
            # print('Test : ' + class_test)
            # print('Predict : ' + class_predict)
            correct += 1 if class_test == class_predict else 0
        accuracy = correct/len(data_tests)
        total_accuracy += accuracy
        print('Akurasi ke-' + str(id_group+1) + ' : ' + str(accuracy))
    print('Rata-rata akurasi : ' + str(total_accuracy/k_fold))