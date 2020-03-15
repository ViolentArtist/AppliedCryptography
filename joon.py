# Joon Hwang
def prep_trials(ciphertext):
    # for key length t{1-24}
    trials = []
    for i in range(1, 25):
        trial_t = []
        for i2 in range(i):
            trial_t.append([])
        trials.append(trial_t)

    for i in range(len(ciphertext)):
        for i2 in range(len(trials)):
            t = i2 + 1
            trials[i2][i % t].append(ciphertext[i])

    return trials


# Joon Hwang
def index_of_coincidence(ciphertext):
    trials = prep_trials(ciphertext)
    iocs = []
    for i in range(len(trials)):
        # within each group per key length t, calculate the index of coincidence
        # average the indices of coincidence across groups per key length t
        t = i + 1
        ioc_sum = 0
        for bucket in trials[i]:
            freq_dict = {}
            for char in bucket:
                if char in freq_dict.keys():
                    freq_dict[char] += 1
                else:
                    freq_dict[char] = 1

            ioc = 0
            N = len(bucket)
            for char in freq_dict:
                ioc += (freq_dict[char] * (freq_dict[char] - 1)) / (N * (N - 1))
            ioc_sum += ioc
        ioc_average = ioc_sum / t
        iocs.append((ioc_average, t))
    print(iocs)


index_of_coincidence('gunfights outjuts molters forgot bedclothes cirrus servomotors tumulus incompleteness provoking '
                     'sixteens breezeways layoff marinas directives teabowl vugs mainframe gazebo bushwhacks testers '
                     'incompressibility unthoughtfully rivalled repaint nonuple guerre semiaquatic flashgun esthetics '
                     'icefall touchups baltic baba gorget groper remittances nimbus podium reassurance preventable '
                     'overroasts chests interchangeable pentarch doctoring potentiated salts overlay rustled '
                     'recyclability version mottled lee')