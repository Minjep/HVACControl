import pandas as pd
import matplotlib.pyplot as plt

# This script takes a csv file generated during a test
# and creates graphs which all use same timeline as x-axis.

headers = ['n', 't', 'rc_state', 'trt', 'rqf', 'rqt', 't_ao', 't_ar', 't_ai', 't_ae', 't_aop', 't_vti', 't_lbi', 't_vto', 't_lbo', 'delta_t_evap', 'ech_1_pct', 'ech_2_pct', 'eev_pct', 'hvac_pct', 'bypass_pct', 'co2_count', 'defrost_state', ]

plt.rcParams["figure.autolayout"] = True

df = pd.read_csv("test_go_to_testmode_forever.csv", names=headers)
dfRL = pd.read_csv("RLvers.csv", names=headers)

#groups = create_groups(headers, known_groups)
#create_graphs(df, groups, MAX_SUBPLOTS_PER_FIGURE)
df['n'] = df['n'] / 60
dfRL['n'] = dfRL['n'] / 60

# Example state mapping (replace with actual states if necessary)
state_mapping = {
    'RC_STATE.INITIAL': 0, 'RC_STATE.RECIRC_COOL': 1,
    'RC_STATE.RECIRC': 2, 'RC_STATE.RECIRC_HEAT': 3,
    'RC_STATE.VENT_COOL': 4, 'RC_STATE.VENT': 5, 'RC_STATE.VENT_HEAT': 6
}

# Assuming rc_state is categorical, map to numerical values
if df['rc_state'].dtype == 'object':
    df['rc_state_mapped'] = df['rc_state'].map(state_mapping)
    dfRL['rc_state_mapped'] = dfRL['rc_state'].map(state_mapping)
else:
    df['rc_state_mapped'] = df['rc_state']
    dfRL['rc_state_mapped'] = dfRL['rc_state']

df['total_power_kW'] = (df['rqf'] * 150 / 100 + df['rqf'] * 150 / 100 +
                        df['ech_1_pct'] * 1150 / 100 + df['ech_2_pct'] * 1150 / 100 +
                        abs(df['hvac_pct']) * 2000 / 100) / 1000
dfRL['total_power_kW'] = (dfRL['rqf'] * 150 / 100 + dfRL['rqf'] * 150 / 100 +
                          dfRL['ech_1_pct'] * 1150 / 100 + dfRL['ech_2_pct'] * 1150 / 100 +
                          abs(dfRL['hvac_pct']) * 2000 / 100) / 1000
df['cumulative_energy_kWh'] = (df['total_power_kW'] * (df['n'].diff().fillna(0) / 60)).cumsum()
dfRL['cumulative_energy_kWh'] = (dfRL['total_power_kW'] * (dfRL['n'].diff().fillna(0) / 60)).cumsum()

# Plot Room Temperature Comparison
plt.figure(figsize=(10, 6))
plt.plot(df['n'], df['t_ar'], label="AM-control")
plt.plot(dfRL['n'], dfRL['t_ar'], label="RL-control")
plt.plot(df['n'], df['trt'], color="red", label="Setpoint")
plt.vlines(15 * 15, ymin=0, ymax=40, linestyles="--", color="grey", label="Disturbance")
plt.legend(loc='best')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlabel("Time[Minutes]", fontsize=11)
plt.ylabel("Temperature[°C]", fontsize=11)
plt.xlim(0, 1000)
plt.ylim(18.9, 27.1)
plt.title("Room temperature comparison on Airmaster simulation tool", fontsize=14)
plt.tight_layout()
plt.savefig("room_temperature_comparison.png")

# Plot CO2 Concentration Comparison
plt.figure(figsize=(10, 6))
plt.plot(df['n'], df['co2_count'], label="AM-control")
plt.plot(dfRL['n'], dfRL['co2_count'], label="RL-control")
plt.vlines(15 * 15, ymin=0, ymax=1500, linestyles="--", color="grey", label="Disturbance")
plt.legend(loc='best')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(0, 1000)
plt.ylim(300, 1500)
plt.xlabel("Time[Minutes]", fontsize=11)
plt.ylabel("CO2 concentration[ppm]", fontsize=11)
plt.title("Room CO2 concentration comparison on Airmaster simulation tool", fontsize=14)
plt.tight_layout()
plt.savefig("co2_concentration_comparison.png")

# Plot RC State Comparison
plt.figure(figsize=(10, 6))
plt.plot(df['n'], df['rc_state_mapped'], label="AM-control")
plt.plot(dfRL['n'], dfRL['rc_state_mapped'], label="RL-control")
plt.legend(loc='best')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(0, 1000)
plt.yticks(ticks=range(len(state_mapping)), labels=["Initial", "Recirculation cooling", "Recirculation", "Recirculation heating", "Ventilation cooling", "Ventilation", "Ventilation Heating"])
plt.ylim(1, 7)
plt.xlabel("Time[Minutes]", fontsize=11)
plt.title("RC State comparison on Airmaster simulation tool", fontsize=14)
plt.tight_layout()
plt.savefig("rc_state_comparison.png")

# Plot Total Power Consumption
plt.figure(figsize=(10, 6))
plt.plot(df['n'], df['total_power_kW'], label="AM-control")
plt.plot(dfRL['n'], dfRL['total_power_kW'], label="RL-control")
plt.xlabel("Time [Minutes]", fontsize=11)
plt.ylabel("Total Power Consumption [kW]", fontsize=11)
plt.title("Estimated total power consumption over time on Airmaster simulation tool", fontsize=14)
plt.legend(loc='best')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(0, 1000)
plt.ylim(0, 3)
plt.tight_layout()
plt.savefig("total_power_consumption.png")

# Plot Cumulative Energy Consumption
plt.figure(figsize=(10, 6))
plt.plot(df['n'], df['cumulative_energy_kWh'], label="AM-control")
plt.plot(dfRL['n'], dfRL['cumulative_energy_kWh'], label="RL-control")
plt.xlabel("Time [Minutes]", fontsize=11)
plt.ylabel("Cumulative Energy Consumption [kWh]", fontsize=11)
plt.title("Estimated cumulative energy consumption over time on Airmaster simulation tool", fontsize=14)
plt.legend(loc='best')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(0, 1000)
plt.ylim(0,6)
plt.tight_layout()
plt.savefig("cumulative_energy_consumption.png")

# Plot AM-control Actuator Percentages
plt.figure(figsize=(10, 6))
plt.plot(df['n'], df['ech_1_pct'], label="ECH 1 %")
plt.plot(df['n'], df['ech_2_pct'], label="ECH 2 %")
plt.plot(df['n'], df['hvac_pct'], label="HVAC %")
plt.plot(df['n'], df['bypass_pct'], label="Bypass %")
plt.plot(df['n'], df['rqf'], label="RQF")
plt.xlabel("Time [Minutes]", fontsize=11)
plt.ylabel("Percentage [%]", fontsize=11)
plt.title("AM-control Actuator Percentages Over Time", fontsize=14)
plt.legend(loc='best')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(0, 1000)

plt.tight_layout()
plt.savefig("am_control_actuator_percentages.png")

# Plot RL-control Actuator Percentages
plt.figure(figsize=(10, 6))
plt.plot(dfRL['n'], dfRL['ech_1_pct'], label="ECH 1 %")
plt.plot(dfRL['n'], dfRL['ech_2_pct'], label="ECH 2 %")
plt.plot(dfRL['n'], dfRL['hvac_pct'], label="HVAC %")
plt.plot(dfRL['n'], dfRL['bypass_pct'], label="Bypass %")
plt.plot(dfRL['n'], dfRL['rqf'], label="RQF")
plt.xlabel("Time [Minutes]", fontsize=11)
plt.ylabel("Percentage [%]", fontsize=11)
plt.title("RL-control Actuator Percentages Over Time", fontsize=14)
plt.legend(loc='best')
plt.grid(True, linestyle='--', alpha=0.7)
plt.xlim(0, 1000)
plt.tight_layout()
plt.savefig("rl_control_actuator_percentages.png")

plt.show()
