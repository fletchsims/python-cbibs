from cbibs.buoy import Cbibs

buoy = Cbibs(api_key='')

# print(buoy.get_latest_measurements_all_stations())

res = buoy.get_latest_measurements_one_station('ann')
print(res)
print(len(res['stations']) == 0)
