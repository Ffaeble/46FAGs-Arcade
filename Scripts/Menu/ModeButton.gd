extends Button

func _on_toggled(toggled_on: bool) -> void:
	GlobConf.mode = toggled_on
	if toggled_on:
		print("is true")
		text = "Roguelike"
	else:
		print("is false")
		text = "Roguelite"
