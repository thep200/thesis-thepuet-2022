def main(prd):
    for i in range(10):
        print(i)
        prd.put(i)
    y_hat = [a for a in prd]
    print('\n')
