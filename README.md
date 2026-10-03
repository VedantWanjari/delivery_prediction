# Food Delivery ETA and Late Delivery Prediction

A machine learning project that predicts:

* **Estimated Delivery Time**
* **Late Delivery / Not Late Delivery**

The app takes delivery order details as input and returns:

* predicted delivery time in minutes
* probability of late delivery
* late / not late classification

## Live Demo

Deployed app: [https://delivery-prediction-w6w4.onrender.com/](https://delivery-prediction-w6w4.onrender.com/)

## Dataset

This project uses the Kaggle dataset:

[Food Delivery Orders & ETA Logistics Dataset](https://www.kaggle.com/datasets/razanihababdellatif/food-delivery-orders-and-eta-logistics-dataset)

The dataset is licensed under **CC BY 4.0 Attribution 4.0 International**:

[CC BY 4.0 License](https://creativecommons.org/licenses/by/4.0/)

## License and Attribution

This project uses a dataset licensed under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

Required attribution:

* credit the original dataset author
* include a link to the CC BY 4.0 license
* indicate if changes were made

This repository acknowledges the original dataset and uses it for training machine learning models.
If you reuse this project or its trained models, please keep the dataset attribution intact.

## Models

Two models are used in this project:

1. **Estimated Delivery Time Model**

   * predicts delivery time in minutes
   * evaluated using regression metrics

2. **Late Delivery Model**

   * predicts whether an order will be late
   * evaluated using classification metrics

## Performance

| Model                   |    MAE |   RMSE |     R2 | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
| ----------------------- | -----: | -----: | -----: | -------: | --------: | -----: | -------: | ------: |
| Estimated Delivery Time | 1.3891 | 2.0943 | 0.9735 |      NaN |       NaN |    NaN |      NaN |     NaN |
| Late Delivery           |    NaN |    NaN |    NaN |   0.8155 |    0.7155 | 0.8228 |   0.7654 |  0.9041 |

## Features Used

The models use pre-delivery features such as:

* order hour
* day of week
* weekend flag
* city
* delivery area
* customer age
* customer type
* restaurant type
* restaurant primary category
* restaurant rating
* items count
* subtotal
* discount percent
* tax amount
* service fee
* delivery fee
* order total
* payment method
* tip amount
* distance
* weather
* traffic level
* delivery partner experience
* delivery partner rating
* restaurant preparation time
* order date derived features

The late delivery model does **not** use actual delivery time as an input feature.

## Project Structure

```text
food-delivery-app/
├─ app.py
├─ requirements.txt
├─ Dockerfile
├─ README.md
├─ models/
│  ├─ estimated_delivery_time_model.pkl
│  └─ late_delivery_model_no_eta.pkl
├─ templates/
│  └─ index.html
└─ .gitignore
```

## How to Run Locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app:app --reload
```

Open the app in your browser:

```text
http://127.0.0.1:8000
```

## Docker Run

```bash
docker build -t food-delivery-app .
docker run -p 10000:10000 food-delivery-app
```

## Deploy on Render

This project is designed to run on Render using Docker.

Render setup:

* create a new **Web Service**
* connect your GitHub repo
* choose **Docker**
* deploy using the `Dockerfile`

## Notes

* The app uses dropdowns and validated inputs for the values that exist in the dataset.
* Invalid categorical values are rejected by the backend.
* The city and delivery area fields are linked so only valid areas appear for the selected city.

## Acknowledgements

Dataset source: Kaggle
Original dataset license: CC BY 4.0
