import trackertools

x = trackertools.update_table("SH_QU_0.csv")
x.to_csv("SH_QU_0.csv", index=False)
