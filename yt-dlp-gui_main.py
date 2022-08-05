# From [current UI savefile] import Ui_MainWindow allows the GIU to be used and updated independently
from yt_dlp_gui_v_two import Ui_MainWindow

# For the GUI to work, you need to import the PyQt5 modules.
from PyQt5 import QtWidgets, QtCore, QtGui, QtWidgets

import sys
import subprocess  # Used to run YT-DLP as a subprocess within the GUI
import tempfile  # Used to create a temporary file for the Save URL's output
from timeit import (
    default_timer as timer,
)  # Timer function to calculate the time taken to download the videos

# https://www.youtube.com/watch?v=XXPNpdaK9WA
# https://github.com/yt-dlp/yt-dlp#installation


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.ui.test_button.clicked.connect(self.ErrorDialog)
        self.ui.status_label.setVerticalScrollBar(
            self.ui.status_label_verticalScrollBar
        )

        self.download_path = ""
        self.remux_filetypes = [
            "mp4",
            "mkv",
            "flv",
            "webm",
            "mov",
            "avi",
            "mka",
            "ogg",
            "mp3",
            "aac",
            "m4a",
            "opus",
            "vorbis",
            "flac",
            "alac",
            "wav",
        ]

    # Create a class that Error Dialogs can inherit from
    class ErrorDialog(QtWidgets.QDialog):
        # Display an error dialog
        def __init__(
            self,
            title="Error",
            message="Error",
            extra_info="Please check your inputs and try again.",
        ):
            super().__init__()
            self.ErrorDialog = QtWidgets.QMessageBox()
            self.ErrorDialog.setWindowTitle(f"{title}")
            self.ErrorDialog.setText(f"{message} \n")
            self.ErrorDialog.setInformativeText(extra_info)
            self.ErrorDialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.ErrorDialog.setIcon(
                QtWidgets.QMessageBox.Information
            )  # Error, Question, Warning, Information, Critical
            self.ErrorDialog.exec_()

    class RestartWithWarning(QtWidgets.QDialog):
        def __init__(
            self,
            title="Restarting...",
            message="Are you sure you want to restart?",
            extra_info="This will close the application. Unsaved data and settings will be lost.",
        ):
            super().__init__()
            self.restart_popup = QtWidgets.QMessageBox()
            self.restart_popup.setWindowTitle(f"{title}")
            self.restart_popup.setText(f"{message} \n")
            self.restart_popup.setInformativeText(extra_info)
            self.restart_popup.setStandardButtons(
                QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
            )
            self.restart_popup.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            self.restart_popup.setIcon(
                QtWidgets.QMessageBox.Warning
            )  # Error, Question, Warning, Information, Critical
            self.restart_popup.buttonClicked.connect(self.restart_popup_clicked)
            self.restart_popup.exec_()

        def restart_popup_clicked(self, i):
            self.i = i
            if i.text() == "OK":
                # def restart(self): # This is the function that actually restarts the program
                QtCore.QCoreApplication.quit()
                QtCore.QProcess.startDetached(sys.executable, sys.argv)

    def update_status_display(self, text_to_add):
        previous_text = self.ui.status_label.toPlainText()
        current_text = previous_text + "\n" + text_to_add
        self.ui.status_label.setText(current_text)
        self.ui.status_label.moveCursor(QtGui.QTextCursor.End)

    # Shorten input to 3 decimal places
    def truncate(self, input, decimals=3):
        multiplier = 10**decimals
        return int(input * multiplier) / multiplier

    @QtCore.pyqtSlot()
    def on_browse_folder_button_clicked(self):
        # open a file browser to select a folder
        self.download_path = QtWidgets.QFileDialog.getExistingDirectory(
            None, "Select download folder:"
        )
        self.ui.folder_path_input.setText(
            self.download_path
        ) if self.download_path != "" else None

    @QtCore.pyqtSlot()
    def on_check_filetypes_button_clicked(self):
        urls = self.url_parser()

        if len(urls) == 0:
            self.ErrorDialog(
                "Error", "No URLs Entered", "Please enter at least one URL"
            )
            return
        self.ui.filetype_dropdown.clear()
        self.ui.filetype_dropdown.addItem("BEST")
        video_formats = ["mp4", "flv", "ogg", "webm", "3gp"]
        audio_formats = ["mp3", "aac", "m4a", "opus", "vorbis", "flac", "alac", "webm"]
        used_video_formats = []
        used_audio_formats = []

        for url in urls:
            command = f"yt-dlp -F {url}"
            proc = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )

            if self.ui.audio_only_checkbox.isChecked():
                for i in proc.stdout:
                    if "audio" in i:
                        i = i.split(" ")[1]
                        # print(i)
                        if i in audio_formats and i not in used_audio_formats:
                            used_audio_formats.append(i)
                            self.ui.filetype_dropdown.addItem(i)

            else:
                for i in proc.stdout:
                    if "video" in i:
                        i = i.split(" ")[1]
                        # print(i)
                        if i in video_formats and i not in used_video_formats:
                            used_video_formats.append(i)
                            self.ui.filetype_dropdown.addItem(i)
            proc.wait()
        return

    @QtCore.pyqtSlot()
    def on_audio_only_checkbox_clicked(self):
        if self.ui.audio_only_checkbox.isChecked():
            self.update_status_display("Audio Only: Enabled")
            # self.ui.filetype_dropdown.setEnabled(False)
            self.ui.filetype_dropdown.setCurrentText("BEST")
            self.ui.filetype_dropdown.addItem("")
            self.ui.filetype_dropdown.addItem("")
            self.ui.filetype_dropdown.setItemText(1, "mp3")
            self.ui.filetype_dropdown.setItemText(2, "aac")
            self.ui.filetype_dropdown.setItemText(3, "m4a")
            self.ui.filetype_dropdown.setItemText(4, "opus")
            self.ui.filetype_dropdown.setItemText(5, "vorbis")
            self.ui.filetype_dropdown.setItemText(6, "flac")
            self.ui.filetype_dropdown.setItemText(7, "alac")
            self.ui.audio_quality_slider.setEnabled(True)

        else:
            self.update_status_display("Audio Only: Disabled")
            # self.ui.filetype_dropdown.setEnabled(True)
            self.ui.filetype_dropdown.setCurrentText("BEST")
            self.ui.filetype_dropdown.setItemText(1, "mp4")
            self.ui.filetype_dropdown.setItemText(2, "flv")
            self.ui.filetype_dropdown.setItemText(3, "ogg")
            self.ui.filetype_dropdown.setItemText(4, "webm")
            self.ui.filetype_dropdown.setItemText(5, "3gp")
            self.ui.filetype_dropdown.removeItem(6)
            self.ui.filetype_dropdown.removeItem(6)
            self.ui.audio_quality_slider.setEnabled(False)

    @QtCore.pyqtSlot()
    def on_download_button_clicked(self):
        try:
            urls = self.url_parser()  # Get the URLs from the input
            # Check if both the download folder and the URL strings are empty
            if len(self.download_path) == 0 and len(urls) == 0:
                self.update_status_display("Download Folder: No Folder Selected")
                self.update_status_display("Download Failed")
                self.ErrorDialog(
                    "Error",
                    "No URL or Save Folder Entered",
                    "Please enter at least one URL and specify the download folder",
                )
                return
            # Check if the download path string is empty
            if len(self.download_path) == 0:
                self.update_status_display("Download Folder: No Folder Selected")
                self.update_status_display("Download Failed")
                self.ErrorDialog(
                    "Error",
                    "No Download Path Selected",
                    "Please select a download folder",
                )
                return
            # Check if the URL string is empty # Check that there is at least one URL
            if len(urls) == 0:
                self.update_status_display(f"Download Folder: {self.download_path}")
                self.update_status_display("Download Failed")
                self.ErrorDialog(
                    "Error", "No URL Entered", "Please enter at least one URL"
                )
                return

            else:
                # If no problems, update the status display with selected options, filetype and download folder
                self.option_compiler()
                options = self.option_output
                self.update_status_display(f"Current Options: {options}")
                self.update_status_display(
                    f"Filetype: {self.ui.filetype_dropdown.currentText()}"
                )
                self.update_status_display(f"Download Folder: {self.download_path}")

                # Variables to update progress bar; current_url_number = current url being downloaded; url_total = total number of urls to download
                current_url_number = 0
                url_total = len(urls)

                # Start Download Timer
                start = timer()

                # Loop through the URLs
                for url in urls:
                    per_url_start = timer()
                    title_count_per_url = 0  # variable that iterates when the title of the video has been displayed, to prevent duplicate printouts
                    current_url_number += 1
                    command = f"yt-dlp {options} {url}"
                    self.update_status_display(
                        f"Downloading URL {current_url_number} of {url_total}: {url}"
                    )

                    # Update label above progress bar with current URL number out of total URLs
                    self.ui.progress_label.setText(
                        f"Downloading {current_url_number} of {url_total}"
                    )
                    self.ui.progress_label.repaint()

                    # Run the command
                    proc = subprocess.Popen(
                        command,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True,
                    )

                    # Loop through the output of the command
                    for i in proc.stdout:
                        # Get the title of the video
                        if (
                            "Destination:" in i and title_count_per_url < 1
                        ):  # get title and prevent duplicate printouts of title
                            i = i.split("Destination: ")[1]
                            i = i[len(self.output_path) + 1 :]
                            i.strip(" ")
                            self.update_status_display(f"Title: {i}")
                            title_count_per_url = 1

                        # Get the progress of the download
                        if "%" in i:
                            i = i.split("[download]")[1]
                            i = i.split("%")[0]
                            i = i.strip(" ")
                            self.ui.progressBar.setProperty("value", float(i))
                            self.ui.progressBar.repaint()

                    # proc.wait()
                    proc.kill()

                    # Stop Download Timer (output in seconds)
                    per_url_elapsed_time = timer() - per_url_start
                    per_url_elapsed_time = self.truncate(per_url_elapsed_time)
                    self.update_status_display(
                        f"URL {current_url_number} completed in {per_url_elapsed_time} seconds"
                    )

                # Stop Download Timer (output in seconds)
                elapsed_time = timer() - start
                elapsed_time = self.truncate(elapsed_time)

                # Display elapsed time and comletion messages
                if url_total == 1:
                    self.update_status_display(
                        f"Download completed in {elapsed_time} seconds"
                    )
                else:
                    self.ui.progress_label.setText(
                        f"Completed {current_url_number} of {url_total} downloads in {elapsed_time} seconds"
                    )
                self.update_status_display("Download Complete")
                self.update_status_display(
                    f"Total Download Time: {elapsed_time} seconds"
                )

                # Reset the progress bar
                self.ui.progressBar.setProperty("value", 0)

        except AttributeError as a:
            self.update_status_display("Download Folder: No Folder Selected")
            self.update_status_display("Download Failed; Attribute Error")
            self.update_status_display(str(a))
            self.ErrorDialog("Error", "Attribute Error", str(a))

        except Exception as e:
            self.update_status_display("Error")
            self.update_status_display("Download Failed")
            self.update_status_display(str(e))
            self.ErrorDialog("Error", "Error", str(e))

    def url_parser(self):
        # check if the url is valid, whether or not it's a playlist, and format it accordingly
        self.legal_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&'()*+,;="
        # reserved_chars   = ";/?:@&=+$,"

        self.urls = self.ui.url_input.document().toPlainText()
        self.urls = self.urls.split(",")
        self.urls = [x.strip() for x in self.urls]

        for url in self.urls:
            if len(url) == 0:
                self.urls.remove(url)
            for char in url:
                if char not in self.legal_characters:
                    self.update_status_display(f"Invalid URL: {url}")
                    self.update_status_display(f"Invalid Characters in URL: {char}")

                    self.urls.strip(url)
                    self.update_status_display("URL Removed")
                    break
        return self.urls

    # Compile the users options into a string

    def get_general_options(self):
        # General Tab

        # if self.ui.ignore_all_config_files_checkBox.isChecked():
        #    #self.option_option_output += "--no-config-locations "
        #    pass
        if self.ui.ignore_config_except_default_checkBox.isChecked():
            self.option_output += "--ignore-config "
        if self.ui.stop_on_error_checkBox.isChecked():
            self.option_output += "--abort-on-error "
        if self.ui.force_generic_extractor_checkBox.isChecked():
            self.option_output += "--force-generic-extractor "
        if self.ui.list_playlist_contents_only_checkBox.isChecked():
            self.option_output += "--flat-playlist "
        if self.ui.livestreams_from_start_checkBox.isChecked():
            self.option_output += "--live-from-start "
        if self.ui.wait_for_streams_checkBox.isChecked():
            self.option_output += "--wait-for-video 10 "
        if self.ui.mark_video_watched_checkBox.isChecked():
            self.option_output += "--mark-watched "
        if self.ui.color_codes_checkBox.isChecked():
            self.option_output += "--no-colors "
        if self.ui.update_checkBox.isChecked():
            self.option_output += "--update "

    def get_netgeo_options(self):
        # Net/Geo Tab
        if self.ui.proxy_url_input.text() != "":
            self.option_output += f"--proxy {self.ui.proxy_url_input.text()} "
        if self.ui.timeout_seconds_input.text() != "":
            self.option_output += (
                f"--socket-timeout {self.ui.timeout_seconds_input.text()} "
            )
        if self.ui.ip_input.text() != "":
            self.option_output += f"--source-address {self.ui.ip_input.text()} "
        if self.ui.force_ipv4_checkBox.isChecked():
            self.option_output += "--force-ipv4 "
        if self.ui.force_ipv6_checkBox.isChecked():
            self.option_output += "--force-ipv6 "
        if self.ui.geo_veri_proxy_url_input.text() != "":
            self.option_output += (
                f"--geo-verification-proxy {self.ui.geo_veri_proxy_url_input.text()} "
            )
        if not self.ui.geo_bypass_checkBox.isChecked():
            self.option_output += "--no-geo-bypass "
        if self.ui.geo_bypass_country_code_input.text() != "":
            self.option_output += (
                f"--geo-bypass-country {self.ui.geo_bypass_country_code_input.text()} "
            )
        if self.ui.geo_bypass_ip_block_input.text() != "":
            self.option_output += (
                f"--geo-bypass-ip {self.ui.geo_bypass_ip_block_input.text()} "
            )

    def get_video_options(self):
        # Video Tab
        if self.ui.playlist_items_input.text() != "":
            self.option_output += (
                f"--playlist-items {self.ui.playlist_items_input.text()} "
            )
        if self.ui.minimum_filesize_input.text() != "":
            self.option_output += (
                f"--min-filesize {self.ui.minimum_filesize_input.text()} "
            )
        if self.ui.maximum_filesize_input.text() != "":
            self.option_output += (
                f"--max-filesize {self.ui.maximum_filesize_input.text()} "
            )
        if self.ui.specific_date_input.text() != "":
            self.option_output += f"--date {self.ui.specific_date_input.text()} "
        if self.ui.before_date_input.text() != "":
            self.option_output += f"--datebefore {self.ui.before_date_input.text()} "
        if self.ui.after_date_input.text() != "":
            self.option_output += f"--dateafter {self.ui.after_date_input.text()} "
        if self.ui.filters_input.text() != "":
            self.option_output += f"--match-filters {self.ui.filters_input.text()} "
        if self.ui.age_limit_input.text() != "":
            self.option_output += f"--age-limit {self.ui.age_limit_input.text()} "

    def get_download_options(self):
        # Download Tab
        if self.ui.max_download_rate_input.text() != "":
            self.option_output += (
                f"--limit-rate {self.ui.max_download_rate_input.text()} "
            )
        if self.ui.retries_input.text() != "":
            self.option_output += f"--retries {self.ui.retries_input.text()} "
        if self.ui.file_access_retries_input.text() != "":
            self.option_output += (
                f"--file-access-retries {self.ui.file_access_retries_input.text()} "
            )
        if self.ui.fragment_retries_input.text() != "":
            self.option_output += (
                f"--fragment-retries {self.ui.fragment_retries_input.text()} "
            )
        if self.ui.retry_sleep_input.text() != "":
            self.option_output += f"--retry-sleep {self.ui.retry_sleep_input.text()} "
        if self.ui.concurrent_frags_input.text() != "":
            self.option_output += (
                f"--max-concurrent-downloads {self.ui.concurrent_frags_input.text()} "
            )
        if self.ui.buffer_size_input.text() != "":
            self.option_output += f"--buffer-size {self.ui.buffer_size_input.text()} "
        if self.ui.download_sections_input.text() != "":
            self.option_output += (
                f"--download-sections {self.ui.download_sections_input.text()} "
            )
        if self.ui.http_chunk_size_input.text() != "":
            self.option_output += (
                f"--http-chunk-size {self.ui.http_chunk_size_input.text()} "
            )
        if self.ui.skip_unavailable_fragments_checkBox.isChecked():
            self.option_output += "--skip-unavailable-fragments "
        if self.ui.abort_on_unavailable_fragments_checkBox.isChecked():
            self.option_output += "--abort-on-unavailable-fragment "
        if self.ui.keep_fragments_checkBox.isChecked():
            self.option_output += "--keep-fragments "
        if self.ui.no_resize_buffer_checkBox.isChecked():
            self.option_output += "--no-resize-buffer "
        if self.ui.playlist_random_checkBox.isChecked():
            self.option_output += "--playlist-random "
        if self.ui.lazy_playlist_checkBox.isChecked():
            self.option_output += "--lazy-playlist "
        if self.ui.use_mpegts_checkBox.isChecked():
            self.option_output += "--hls-use-mpegts "
        if self.ui.no_use_mpegts_checkBox.isChecked():
            self.option_output += "--no-hls-use-mpegts "

    def option_compiler(self):
        self.option_output = ""
        self.get_general_options()
        self.get_netgeo_options()
        self.get_video_options()
        self.get_download_options()

        # Add user selected path to the option_output
        self.output_path = self.ui.folder_path_input.text()
        self.option_output = f"{self.option_output} -P {self.output_path} "
        self.audio_only = self.ui.audio_only_checkbox.isChecked()

        # Add user selected file format to the option_output
        self.filetype = self.ui.filetype_dropdown.currentText()

        audio_quality = str(self.ui.audio_quality_slider.value())

        if self.audio_only and (self.filetype == "BEST"):
            self.option_output += "--extract-audio "
            self.option_output += f"--audio quality {audio_quality} "
            self.option_output += f"--remux-video {self.filetype} "
        if self.audio_only and (self.filetype != "BEST"):
            self.option_output += f"-extract-audio --audio-format {self.filetype} "
            self.option_output += f"--audio quality {audio_quality} "
            self.option_output += f"--remux-video {self.filetype} "

        # May be a better way to do this, but I'm not sure how
        if self.audio_only or self.filetype != "BEST":
            self.option_output = f"{self.option_output} --format {self.filetype} "

        # self.option_output = f"{self.option_output} --video-multistreams "
        # self.option_output = f"{self.option_output} --audio-multistreams "

        return self.option_output

    # Utilities Tab
    @QtCore.pyqtSlot()
    def on_restart_button_clicked(self):
        self.RestartWithWarning()

    @QtCore.pyqtSlot()
    def on_load_urls_button_clicked(self):
        url_list = []
        try:
            with open(self.temp.name, "r") as listfile:
                url_list.extend(iter(listfile))
            listfile.close()
            self.ui.url_input.setPlainText("".join(url_list))
        except Exception:
            print("No URL list found")
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
        return

    @QtCore.pyqtSlot()
    def on_save_urls_button_clicked(self):
        urls = self.url_parser()
        # path = self.ui.folder_path_input.text()
        # with open(path, "w") as listfile:
        #    listfile.write(urls)
        # listfile.close()
        self.temp = tempfile.NamedTemporaryFile(
            prefix="yt-dlp-gui_", suffix=".txt", delete=False
        )
        try:
            with open(self.temp.name, "w") as listfile:
                for url in urls:
                    if len(url) > 0:
                        listfile.write(f"{url}, \n")
            listfile.close()
        except Exception:
            print("Error saving list")
            self.ErrorDialog = QtWidgets.QMessageBox()
            self.ErrorDialog.setWindowTitle("Error")
            self.ErrorDialog.setText("Error saving list")
            self.ErrorDialog.setInformativeText("Please check the path and try again.")
            self.ErrorDialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.restart_warning.exec_()
        # temp.write(urls)
        # print("Could not create temporary file")

        print("Created file is:", self.temp)
        print("Name of the file is:", self.temp.name)
        self.temp.close()

    @QtCore.pyqtSlot()
    def on_add_config_file_button_clicked(self):
        # open a file browser to select a folder
        self.config_path = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select configuration file:"
        )
        self.config_path = self.config_path[0]
        self.ui.config_label.setText(f"Config File: {self.config_path}")
        if len(self.config_path) > 0:
            self.ui.ignore_all_config_files_checkBox.setChecked(False)
        else:
            self.ui.ignore_all_config_files_checkBox.setChecked(True)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
