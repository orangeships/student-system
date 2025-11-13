"""
修复Python 3.12中statistics模块缺少函数的问题
"""
import statistics
import math

# 修复mean函数
if not hasattr(statistics, 'mean'):
    def mean(data):
        """计算平均值"""
        if not data:
            raise statistics.StatisticsError('mean requires at least one data point')
        return sum(data) / len(data)
    statistics.mean = mean

# 修复stdev函数
if not hasattr(statistics, 'stdev'):
    def stdev(data, mu=None):
        """计算样本标准差"""
        if not data:
            raise statistics.StatisticsError('stdev requires at least one data point')
        if len(data) < 2:
            raise statistics.StatisticsError('stdev requires at least two data points')
        if mu is None:
            mu = statistics.mean(data)
        variance = sum((x - mu) ** 2 for x in data) / (len(data) - 1)
        return math.sqrt(variance)
    statistics.stdev = stdev

# 修复pstdev函数
if not hasattr(statistics, 'pstdev'):
    def pstdev(data, mu=None):
        """计算总体标准差"""
        if not data:
            raise statistics.StatisticsError('pstdev requires at least one data point')
        if mu is None:
            mu = statistics.mean(data)
        variance = sum((x - mu) ** 2 for x in data) / len(data)
        return math.sqrt(variance)
    statistics.pstdev = pstdev

# 修复pvariance函数
if not hasattr(statistics, 'pvariance'):
    def pvariance(data, mu=None):
        """计算总体方差"""
        if not data:
            raise statistics.StatisticsError('pvariance requires at least one data point')
        if mu is None:
            mu = statistics.mean(data)
        return sum((x - mu) ** 2 for x in data) / len(data)
    statistics.pvariance = pvariance

# 修复variance函数
if not hasattr(statistics, 'variance'):
    def variance(data, mu=None):
        """计算样本方差"""
        if not data:
            raise statistics.StatisticsError('variance requires at least one data point')
        if len(data) < 2:
            raise statistics.StatisticsError('variance requires at least two data points')
        if mu is None:
            mu = statistics.mean(data)
        return sum((x - mu) ** 2 for x in data) / (len(data) - 1)
    statistics.variance = variance

print("成功修复statistics模块的函数")