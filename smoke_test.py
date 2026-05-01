from predictor import predict_top3
r = predict_top3(90, 42, 43, 20.87, 82, 6.5, 202.9)
for c in r['top3']:
    print(f"#{c['rank']} {c['crop']:15s} conf={c['confidence']}%  price=Rs{c['price']}")
print("Soil:", r['soil_health']['status'])
print("Crops:", r['crops_list'][:5], "...")
