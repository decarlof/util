
nAngles = 1000

def sine_fun(X, amp, phi, y_offset):
    return amp * np.sin(np.radians(X+ phi)) + y_offset


# make data:
x = np.linspace(0,360,nAngles)
amp= 10
phi = 75
y_offset = 5
data = sine_fun(x, amp, phi, y_offset) + np.random.normal(0, 0.1, nAngles)



amp_st = np.max(data)*2
w_st = 1
phi_st = 23
y_offset_st = np.mean(data)
popt = curve_fit(sine_fun,x,data,p0=[amp_st, phi_st, y_offset_st]) # gaussian fit on the derivative of raw data
fit_param = popt[0]
amp_fit = fit_param[0]
phi_fit = fit_param[1]
y_offset_fit = fit_param[2]
Sine_fit = sine_fun(x, amp_fit, phi_fit, y_offset_fit)

print 'Amplitude: %i' % amp_fit
print 'dephasage: %i' % phi_fit
print 'vert. offset: %i' % y_offset_fit

plt.plot(x, data, 'b.')
plt.hold, plt.plot(x, Sine_fit, 'r-'), plt.grid()
plt.show()





