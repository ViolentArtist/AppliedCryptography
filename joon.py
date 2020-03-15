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
# returns the three top key lengths based on how similar the respective index of coincidence is to that of the English
# language
def index_of_coincidence_analysis(ciphertext):
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
                if N > 1:
                    ioc += (freq_dict[char] * (freq_dict[char] - 1)) / (N * (N - 1))
            ioc_sum += ioc
        ioc_average = ioc_sum / t
        iocs.append((ioc_average, t))
    ioc_diffs = [(abs(ioc[0] - 0.06), ioc[1]) for ioc in iocs]
    return sorted(ioc_diffs)[:3]


# Joon Hwang
def chi_squared_analysis(ciphertext, key_length):
    english_percents = {' ': 0.1829, 'a': 0.0653, 'b': 0.0126, 'c': 0.0223, 'd': 0.0328, 'e': 0.1027, 'f': 0.0198,
                        'g': 0.0162, 'h': 0.0498, 'i': 0.0567, 'j': 0.0010, 'k': 0.0056, 'l': 0.0332, 'm': 0.0203,
                        'n': 0.0571, 'o': 0.0616, 'p': 0.0150, 'q': 0.0008, 'r': 0.0499, 's': 0.0532, 't': 0.0752,
                        'u': 0.0228, 'v': 0.0080, 'w': 0.0170, 'x': 0.0014, 'y': 0.0143, 'z': 0.0005}
    buckets = []
    for i in range(key_length):
        buckets.append([])
    for i in range(len(ciphertext)):
        buckets[i % key_length].append(ciphertext[i])

    key = []
    total_chi_squared = 0
    for bucket in buckets:
        shift_buffer = ''
        chi_buffer = []
        for shift_amount in range(1, 26):
            freq_dict = {}
            chi_squared = 0
            chi_shift = []

            # shift by once every iteration to make things simple
            if len(shift_buffer) == 0:
                for char in bucket:
                    if char == ' ':
                        shift_buffer += 'a'
                    elif char == 'z':
                        shift_buffer += ' '
                    else:
                        shift_buffer += chr(ord(char) + 1)
            else:
                temp = ''
                for char in shift_buffer:
                    if char == ' ':
                        temp += 'a'
                    elif char == 'z':
                        temp += ' '
                    else:
                        temp += chr(ord(char) + 1)
                shift_buffer = temp

            for char in shift_buffer:
                if char in freq_dict.keys():
                    freq_dict[char] += 1
                else:
                    freq_dict[char] = 1

            for char in freq_dict.keys():
                char_chi_squared = ((freq_dict[char] - english_percents[char] * len(bucket)) ** 2) / \
                                   (english_percents[char] * len(bucket))
                chi_squared += char_chi_squared

            # record chi-squared values for different shift amounts
            chi_buffer.append((chi_squared, shift_amount))
        key.append(sorted(chi_buffer)[0][1])
        total_chi_squared += sorted(chi_buffer)[0][0]
    return key, total_chi_squared

def main():
    # input ciphertext
    ciphertext = "sinbyqbenfbka ahdahqhz ajasdgkkkkkaskdkgi"
    top_key_lengths = index_of_coincidence_analysis(ciphertext)
    print("Probable keys and their associated chi-squared values")
    for i in range(3):
        print(chi_squared_analysis(ciphertext, top_key_lengths[i][1]))

main()