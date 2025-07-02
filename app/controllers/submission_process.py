import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from app.helpers.response_reapper import response_wrapper


def preprocess_data(df):
    scaler = MinMaxScaler()
    df['normalized_type'] = scaler.fit_transform(df[['type']])
    df['normalized_concern'] = scaler.fit_transform(df[['concern']])
    df['normalized_price'] = scaler.fit_transform(df[['price']])
    df['normalized_recommend'] = scaler.fit_transform(df[['recommend']])

    return df


def weight_scoring_process(df, weights=None):
    # Default weights if not provided
    if weights is None:
        weights = {'type': 0.3, 'concern': 0.3,
                   'price': 0.25, 'recommend': 0.15}

    # Calculate weighted score
    df['score'] = (weights['type'] * df['normalized_type']) + (weights['concern'] * df['normalized_concern']) + \
        (weights['price'] * df['normalized_price']) + \
        (weights['recommend'] * df['normalized_recommend'])

    # Get top N recommendations
    recommendations = df.sort_values(by='score', ascending=False)

    return recommendations[['id', 'type', 'concern', 'price', 'recommend', 'score']]


def normalize_data(value, weight):
    # normalization

    wMin = min(weight)
    wMax = max(weight)

    if wMax - wMin != 0:
        normalized = (value - wMin) / (wMax - wMin)
    else:
        normalized = value * 0
    return normalized


def scoring_userdata(user_input, weights):
    cWeight = {'type': 0.3, 'concern': 0.3, 'price': 0.25, 'recommend': 0.15}

    nType = normalize_data(user_input['type'], weights['type'])
    nConcern = normalize_data(user_input['type'], weights['concern'])
    nPrice = normalize_data(user_input['price'], weights['price'])
    nRecommend = normalize_data(user_input['recommend'], weights['recommend'])

    userScore = (nType * cWeight['type']) + (nConcern * cWeight['concern']) + (
        nPrice * cWeight['price']) + (nRecommend * cWeight['recommend'])
    return userScore


def main_process(data, weights, user_input):
    try:
        df = pd.DataFrame(data)
        df = preprocess_data(df)

        all_recommendation = weight_scoring_process(df)
        user_score = scoring_userdata(user_input, weights)
        recommended_product_id = all_recommendation.loc[(
            all_recommendation['score'] - user_score).abs().idxmin(), 'id']
        response = {
            'recommended_id': recommended_product_id
        }
        return response_wrapper(response, 200, 'Ok')
    except Exception as e:
        return response_wrapper({}, 500, e)
