# header
Header      header


# ----------------- drone state ----------------------
UInt8  drone_state

# ----------------- Mobile device and face detection data (Target1 2 3 4) ----------------------
float32 fused_z_orientation	# z axis -ve to the left +ve to the right (Yaw)
float32 fc_bbx_cent_x
float32 fc_bbx_cent_y
float32 fc_bbx_rat

# ----------------- drone observation and Human Dectection data ----------------------
float32 drone_yaw
float32 hu_bbx_cent_x
float32 hu_bbx_cent_y
float32 hu_bbx_rat
