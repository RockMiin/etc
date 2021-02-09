# import ruptures

# def rupture_pkg(df):
#     points= np.array(df['time'])
#     points= df['time']
#
#     # RUPTURES PACKAGE
#     # Changepoint detection with the Pelt search method
#     # model= 'rbf'
#     # algo= rpt.Pelt(model= model).fit(rup_time)
#     # result= algo.predict(pen= 10)
#     # rpt.display(rup_time, result, figsize=(10, 6))
#     # plt.show()
#     #
#     # Changepoint detection with the Binary Segmentation search method
#     # model= 'l2'
#     # algo= rpt.Binseg(model= model).fit(rup_time)
#     # rup_bkps= algo.predict(n_bkps=10)
#     # rpt.show.display(rup_time, rup_bkps, figsize= (10, 6))
#     # plt.show()
#     #
#     # Changepoint detection with window-based search method
#     # model = "l2"
#     # algo = rpt.Window(width=40, model=model).fit(points)
#     # my_bkps = algo.predict(n_bkps=10)
#     # rpt.show.display(points, my_bkps, figsize=(10, 6))
#     # plt.title('Change Point Detection: Window-Based Search Method')
#     # plt.show()
#     #
#     # Changepoint detection with dynamic programming search method
#     # model = "l1"
#     # algo = rpt.Dynp(model=model, min_size=3, jump=5).fit(points)
#     # my_bkps = algo.predict(n_bkps=10)
#     # rpt.show.display(points, my_bkps, figsize=(10, 6))
#     # plt.title('Change Point Detection: Dynamic Programming Search Method')
#     # plt.show()