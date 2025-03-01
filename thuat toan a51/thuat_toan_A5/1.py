class A51:
    def __init__(self, key, frame):
        self.R1 = [0] * 19
        self.R2 = [0] * 22
        self.R3 = [0] * 23
        self.key_setup(key, frame)

    def majority(self, x, y, z):
        return (x & y) | (x & z) | (y & z)

    def shift(self, reg, feedback):
        new_bit = sum([reg[i] for i in feedback]) % 2
        reg.pop()
        reg.insert(0, new_bit)

    def key_setup(self, key, frame):
        # Nạp khóa 64-bit vào 3 thanh ghi
        for i in range(64):
            bit = (key >> i) & 1
            self.R1[0] ^= bit
            self.R2[0] ^= bit
            self.R3[0] ^= bit
            self.shift(self.R1, [13, 16, 17, 18])
            self.shift(self.R2, [20, 21])
            self.shift(self.R3, [7, 20, 21, 22])

        # Nạp số khung 22-bit vào 3 thanh ghi
        for i in range(22):
            bit = (frame >> i) & 1
            self.R1[0] ^= bit
            self.R2[0] ^= bit
            self.R3[0] ^= bit
            self.shift(self.R1, [13, 16, 17, 18])
            self.shift(self.R2, [20, 21])
            self.shift(self.R3, [7, 20, 21, 22])

        # Đồng bộ hóa
        for _ in range(100):
            maj = self.majority(self.R1[8], self.R2[10], self.R3[10])
            if self.R1[8] == maj:
                self.shift(self.R1, [13, 16, 17, 18])
            if self.R2[10] == maj:
                self.shift(self.R2, [20, 21])
            if self.R3[10] == maj:
                self.shift(self.R3, [7, 20, 21, 22])

    def get_keystream(self, length):
        keystream = []
        for _ in range(length):
            maj = self.majority(self.R1[8], self.R2[10], self.R3[10])
            if self.R1[8] == maj:
                self.shift(self.R1, [13, 16, 17, 18])
            if self.R2[10] == maj:
                self.shift(self.R2, [20, 21])
            if self.R3[10] == maj:
                self.shift(self.R3, [7, 20, 21, 22])
            keystream.append(self.R1[-1] ^ self.R2[-1] ^ self.R3[-1])
        return keystream

# Ví dụ sử dụng
key = 0b1100110011001100110011001100110011001100110011001100110011001100
frame = 0b1010101010101010101010
a51 = A51(key, frame)
keystream = a51.get_keystream(114)  # Sinh 114 bit keystream
print(keystream)
