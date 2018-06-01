# Today's Photos

Easy to use python script that gets today's (or from any other day) photos from your camera and puts them into your photo folder.

Once you've setup your **config.json** file it can be as easy as

```
todaysphotos
```

and all your photos from today are backupped to your *photo folder* named as today's date according to the *date format* you've set in your **config.json**.

Further possibilities are

```
todaysphotos --type Travel --name Kyoto
```

and your photos from today are stored in a folder called `<todays date> | Travel | Kyoto`. The delimiter *|* can be changed in the **config.json** as well.

## Config

Modify the configuration file to your needs

```
{
	"target_folders": [
		"01 Deselect",
		"02 Select",
		"03 Edit",
		"04 Export"
	],
	"export_folder": "01 Deselect",
	"source_dir": "/Volumes/EOS_DIGITAL/DCIM/100CANON",
	"destination_dir": "/Volumes/ExternalDrive/Photography",
	"date_format": "%Y.%m.%d",
	"export_folder_delimiter": " | "
}

```

* `target_folders` Subfolders that should be created in the output folders, can be empty
* `export_folder` The folder the images should be stored in. Can be one of the *target_folders* or a new one
* `source_dir` Path to your SD Card
* `destination_dir` Path to your usual backup drive's photo directory
* `date_format` string to format the date just like in the python [datetime module](https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior)
* `export_folder_delimiter` seperator between *date*, *type* and *name*

## Options

| Option               | Value                            | Description                                                                                   |
|----------------------|----------------------------------|-----------------------------------------------------------------------------------------------|
| `-d`, `--date`       | `today` `yesterday` `YYYY-MM-DD` | Date for the photos to backup. Defaults to *today*                                            |
| `-n`, `--name`       | String                           | Name of the photoshoot for the output folder                                                  |
| `-t`, `--type`       | String                           | Type of the photoshoot for the output folder. For example *Travel*, *Landscape* or *Portrait* |
| `-r`, `--remove-orig` | None                             | If set the original images will be deleted                                                    |
| `-o`, `--output`     | Directory                        | Output directory that overwrites the one set in the **config.json**                           |


## Folder Structure

## With JPGs

```
- destination_dir
	|- export_folder
  		|- JPG
   			|- JPG 1
      			...
   			|- JPG n
  		|- RAW
   			|- RAW 1
     			...
   			|- RAW n
 	|- target_folder 1
         ...
 	|- target_folder n   	  
```

## Without JPGs

```
- destination_dir
	|- export_folder
		|- Photo 1
      		...
  		|- Photo n
 	|- target_folder 1
    	...
 	|- target_folder n   	  
```

## Install

Download the latest release from the [release page](https://github.com/00SteinsGate00/Todays-Photos/releases) and copy it to somewhere in your path, for example `usr/local/bin`

Modify the [example_config.json](example_config.json) to your needs and store it at `$HOME/.todaysphotos_config.json`.

You're good to go!


## Example

Backup your portrait session from today

```
todaysphotos --type Portrait --name "Golden Hour Shoot"
```

You've been shooting landscapes yesterday?

```
todaysphotos --date yesterday --type Landscape --name Lafoten
```

Some images from last week you haven't backed up yet?

```
todaysphotos --date 2018-05-25 --type Travel --name Germany --remove_orig
```



## Licence

[MIT](licence.md)
