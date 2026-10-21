---
title: Rsync & Rclone Syncing
keywords: [computer reference, linux, copypasta, rsync, rclone]
date: 2026-06-23 10:21:00
abstract: Setting up for transfer and synchronization of a portable NVMe M.2 (2 TB) with an internal SATA SSD. Both drives are formatted exFAT. My desktop currently runs Windows and Linux (separate NVMe M.2 drives), and both access and manage files on the SATA SSD, which I use as my personal archive.
---

**WARNING:** Rsync is **one-way only**! This will sync from the internal to the external. It is **not** bidirectional. The order of the drives in the commands provided can be reversed to sync in the other direction, but rsync **cannot** do bidirectional syncing.

**Objective:** Set up syncing between internal archive SATA SSD with external NMVe M.2 SSD in Fedora Kinoite.

## Rsync

Begin by formatting external drive to exFAT.

Due to exFAT formatting, do not use the standard `-a` archive flag as this includes group/owner/permission flags, which will not work on exFAT.

Ensure both drives are mounted.

Try:

```bash
rsync -rtvhi --modify-window=1 --dry-run /run/media/bonju/SSD/ /run/media/bonju/external2tb/
```

* **`-r`:** Recursive, copies subdirectories and files within.
* **`-t`:** Preserve modification times.
* **`-v`:** Verbose, print every filename to the terminal during transfer.
* **`-h`:** Human-readable, format sizes and transfer speeds into easily readable units instead of byte strings.
* **`--progress`:** Display progress and estimate time remaining.
* **`--i`:** Itemized change reasoning, decipherable if needed.
* **`--modify-window=1`:** Linux/macOS record nanosecond timestamps, but Windows exFAT resolution is only 2 seconds. This forces rsync to ignore 1-second timestamp differences.
* **`--dry-run`:** Test-drive, without any actual copying, to preview effect. Delete this when output is correct.

Once the output looks perfect, run:

```bash
rsync -rtvhi --modify-window=1 /run/media/bonju/SSD/ /run/media/bonju/external2tb/
```

## Rclone

**Important:** I have not tested this yet.

Once the initial sync is complete with `rsync`, it is viable to do the same thing with rclone, but bidirectionally. This requires an initial run using the `--resync` flag to initialize the rclone state on the OS as follows:

```bash
rclone bisync /run/media/bonju/SSD/ /run/media/bonju/external2tb/ \
  --modify-window 2s \
  --verbose \
  --progress \
  --resync \
  --dry-run
```

Following the initialization, the command can be altered to:

```bash
rclone bisync /run/media/bonju/SSD/ /run/media/bonju/external2tb/ \
  --modify-window 2s \
  --verbose \
  --progress \
  --check-access \
  --conflict-resolve newer \
  --dry-run
  ```

*In the above examples, remove the `--dry-run` once output looks accurate.*

## Windows

Rclone will also work from Windows, if installed. The file paths will need to be changed appropriately to Windows format (though Rclone can use forward slashes natively), and the `--resync` command would need to be used for the intitial sync **each time the OS is switched**. Line continuations in Powershell are accomplished with `` ` `` instead of `\` as on Linux.
