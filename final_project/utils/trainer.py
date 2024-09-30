from sklearn.kernel_ridge import KernelRidge


class Estimator:
    @staticmethod
    def fit(train_x, train_y):
        return KernelRidge(alpha=0.6, kernel='polynomial', degree=2, coef0=2.5).fit(train_x, train_y)

    @staticmethod
    def predict(trained, test_x):
        return trained.predict(test_x)