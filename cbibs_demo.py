from cbibs.buoy import Cbibs

buoy = Cbibs(api_key='')

# print(buoy.get_latest_measurements_all_stations())

res = buoy.get_current_readings_all_stations()
print(res)
