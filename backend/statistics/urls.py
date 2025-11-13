from django.urls import path
from . import views

urlpatterns = [
    # 统计分析接口
    path('statistics/summary/', views.StatisticsSummaryView.as_view(), name='statistics-summary'),
    path('statistics/categories/', views.StatisticsCategoriesView.as_view(), name='statistics-categories'),
    path('statistics/trend/', views.StatisticsTrendView.as_view(), name='statistics-trend'),
    
    # 数据规划接口
    path('planning/prediction/', views.PlanningPredictionView.as_view(), name='planning-prediction'),
    path('planning/recommendations/', views.PlanningRecommendationsView.as_view(), name='planning-recommendations'),
]