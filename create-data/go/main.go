package main

import (
	"fmt"
	"github.com/go-rod/rod"
	"github.com/go-rod/rod/lib/launcher"
	"time"
)

func main() {
	count := 0
	for {
		// Randomly choose a device from the list of predefined devices
		//device := devices.LaptopWithTouch

		browser := rod.New().ControlURL(
			launcher.New().Bin("/Applications/Brave Browser.app/Contents/MacOS/Brave Browser").Headless(false).MustLaunch(),
		).MustConnect()

		page := browser.MustPage("http://localhost:63342/create-data/create-data/") //.MustEmulate(device)

		page.MustWaitStable()
		time.Sleep(2 * time.Second)
		fmt.Println("Done with device:") //, device.Title)

		page.MustClose()
		count++
	}
}
