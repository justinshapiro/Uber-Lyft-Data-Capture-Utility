package __UI__;

import javafx.application.Platform;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.concurrent.Service;
import javafx.concurrent.Task;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.*;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.image.*;
import javafx.scene.image.Image;
import javafx.scene.paint.Color;
import javafx.stage.DirectoryChooser;
import javafx.stage.Stage;

import java.awt.*;
import java.io.*;
import java.net.MalformedURLException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.ArrayList;
import java.util.ResourceBundle;

public class Controller implements Initializable {
    @FXML private Label run_status = new Label();
    @FXML private Label path_notify = new Label();
    @FXML private Hyperlink locations_edit = new Hyperlink();
    @FXML private ImageView logo = new ImageView();
    @FXML private ListView<String> selected_locations = new ListView<>();
    @FXML private Button browse_button = new Button();
    @FXML private Button browse_button2 = new Button();
    @FXML private Button start_button = new Button();
    @FXML private Button stop_button = new Button();
    @FXML public TextField d_name = new TextField();
    @FXML public TextField d_location = new TextField();
    @FXML public TextField l_name = new TextField();
    @FXML public TextField l_location = new TextField();
    @FXML private TextArea status_area = new TextArea();

    private Boolean stopped = true;

    @Override
    public void initialize(URL url, ResourceBundle rb) {
        // set resources directory path
        String s = "file:/" + System.getProperty("user.dir") + "/";
        s = s.replaceAll("\\\\", "/");
        final String main_folder_path = s;

        // initialize screen logo
        String logo_path = main_folder_path + "resources/soelogo.png";
        logo_path = logo_path.replaceAll("\\\\", "/");
        logo.setImage(new Image(logo_path));

        // initialize run status indicators
        run_status.setTextFill(Color.web("#ff0000"));
        run_status.setText("Not Running");

        // retrieve user preferences for data file name and location
        try {
            URL prefs_location = new URL(main_folder_path + "resources/preferences.txt");
            BufferedReader prefs = new BufferedReader(new InputStreamReader(prefs_location.openStream()));
            d_name.setText(prefs.readLine());
            d_location.setText(prefs.readLine());
            l_name.setText(prefs.readLine());
            l_location.setText(prefs.readLine());
            prefs.close();
        } catch (IOException e) { status_area.appendText("! Preferences file not found !"); }

        // initialize listener for TextFields
        d_name.textProperty().addListener((observable, oldValue, newValue) -> update_preferences(main_folder_path));
        d_location.textProperty().addListener((observable, oldValue, newValue) -> update_preferences(main_folder_path));
        l_name.textProperty().addListener((observable, oldValue, newValue) -> {
            hyperlink_update();
            update_preferences(main_folder_path);
        });
        l_location.textProperty().addListener((observable, oldValue, newValue) -> {
            hyperlink_update();
            update_preferences(main_folder_path);
        });

        hyperlink_update();

        // initialize the browse buttons to open the system's file explorer to choose a path for the data result file
        DirectoryChooser directory_chooser = new DirectoryChooser();
        Stage stage = new Stage();
        stage.setTitle("Choose Directory");
        directory_chooser.setTitle("Choose Directory File");
        File default_directory = new File(System.getProperty("user.dir"));
        directory_chooser.setInitialDirectory(default_directory);
        browse_button.setOnAction(event -> {
            File selected_directory = directory_chooser.showDialog(stage);
            d_location.setText(selected_directory.toPath().toString());
        });
        browse_button2.setOnAction(event -> {
            File selected_directory = directory_chooser.showDialog(stage);
            l_location.setText(selected_directory.toPath().toString());
        });

        // initialize the START button
        start_button.setOnAction(event -> {
            if (d_name.getText().trim().isEmpty()) {
                Alert alert = new Alert(Alert.AlertType.ERROR);
                alert.setTitle("Error");
                alert.setHeaderText(null);
                alert.setContentText("The \"Data File Name\" field must contain a value before starting the run.");
                alert.showAndWait();
            } else if (l_name.getText().trim().isEmpty()) {
                Alert alert = new Alert(Alert.AlertType.ERROR);
                alert.setTitle("Error");
                alert.setHeaderText(null);
                alert.setContentText("The \"Location File Name\" field must contain a value before starting the run.");
                alert.showAndWait();
            } else if (d_location.getText().trim().isEmpty()) {
                Alert alert = new Alert(Alert.AlertType.ERROR);
                alert.setTitle("ERROR");
                alert.setHeaderText(null);
                alert.setContentText("The \"Data File Folder\" field must contain a value before starting the run");
                alert.showAndWait();
            } else if (l_location.getText().trim().isEmpty()) {
                Alert alert = new Alert(Alert.AlertType.ERROR);
                alert.setTitle("Warning");
                alert.setHeaderText(null);
                alert.setContentText("The \"Location File Folder\" field must contain a value before starting the run");
                alert.showAndWait();
            } else {
                run_status.setTextFill(Color.web("#328332"));
                run_status.setText("Running");
                path_notify.setText("Data collecting at: " + d_location.getText() + "\\" + d_name.getText());
                path_notify.setVisible(true);
                start_button.setDisable(true);
                stop_button.setDisable(false);
                d_name.setDisable(true);
                d_location.setDisable(true);
                l_name.setDisable(true);
                l_location.setDisable(true);
                locations_edit.setDisable(true);
                browse_button.setDisable(true);
                browse_button2.setDisable(true);
                stopped = false;

                new Thread(new Task<Void>() {
                    @Override
                    protected Void call() throws Exception {
                        BufferedReader status_file = null;
                        while (!stopped) {
                            URL status_file_location = new URL(main_folder_path + "resources/status.txt");
                            try {
                                status_file = new BufferedReader(new InputStreamReader(status_file_location.openStream()));
                                String line;
                                while ((line = status_file.readLine()) != null) {
                                    final String str_update = line;
                                    Platform.runLater(() -> {
                                        status_area.appendText(str_update + "\n");
                                    });
                                }

                                Thread.sleep(2700);

                            } catch (IOException e) { status_area.appendText("! query_agent IPC file is missing !\n"); }
                        }

                        try {
                            status_file.close();
                        } catch (NullPointerException e) { /* do nothing, this is related to missing IPC file */ }

                        return null;
                    }
                }).start();
            }

            String l_file = l_location.getText() + "\\" + l_name.getText();
            String d_file = d_location.getText() + "\\" + d_name.getText();
            try {
                new ProcessBuilder("resources\\query_agent.exe", l_file, d_file).start();
            } catch (IOException e) { status_area.appendText("! Fatal Error: query_agent.exe failed to start !\n"); }
        });

        // initialize the STOP button
        stop_button.setOnAction(event -> {
            stopped = true;
            run_status.setTextFill(Color.web("#ff0000"));
            run_status.setText("Not Running");
            path_notify.setVisible(false);
            stop_button.setDisable(true);
            start_button.setDisable(false);
            d_name.setDisable(false);
            d_location.setDisable(false);
            l_name.setDisable(false);
            l_location.setDisable(false);
            locations_edit.setDisable(false);
            browse_button.setDisable(false);
            browse_button2.setDisable(false);

            try {
                Runtime.getRuntime().exec("taskkill /F /IM query_agent.exe");
            } catch (IOException e) { status_area.appendText("! query_agent.exe failed to close !\n"); }
        });
    }

    private void hyperlink_update() {
        // initialize the hyperlink to view/edit the locations.csv in the environment's default viewer
        try {
            URL locations_file = new URL("file:/" + l_location.getText() + "/" + l_name.getText());
            locations_edit.setText("Edit \"" + l_name.getText() + "\"");
            locations_edit.setOnAction(event -> {
                try {
                    try {
                        Desktop.getDesktop().open(new File(locations_file.toURI()));
                    } catch (URISyntaxException e) { status_area.appendText("! URI syntax incorrect !\n"); }
                } catch (IOException ioe) { status_area.appendText("! Locations File Not Found !\n"); }
            });

            // initialize the ListView that shows the current contents of locations.csv
            ArrayList<String> str_list = new ArrayList<>();
            try {
                BufferedReader csv = new BufferedReader(new InputStreamReader(locations_file.openStream()));
                csv.readLine();
                for (String line = csv.readLine(); line != null; line = csv.readLine()) {
                    String[] l = line.split(",");
                    String entry = l[0] + " (" + l[1] + ", " + l[2] + ")";
                    str_list.add(entry);
                }
            } catch (IOException e) { status_area.appendText("! Locations File Not Found !\n"); }
            ObservableList<String> locations = FXCollections.observableArrayList(str_list);
            selected_locations.setItems(locations);
        } catch (MalformedURLException e) { status_area.appendText("! Malformed URL !\n"); }
    }

    private void update_preferences(final String main_folder_path) {
        try {
            try {
                URI prefs_file_location = new URI(main_folder_path + "resources/preferences.txt");
                PrintWriter prefs = new PrintWriter(new File(prefs_file_location), "UTF-8");
                prefs.println(d_name.getText());
                prefs.println(d_location.getText());
                prefs.println(l_name.getText());
                prefs.println(l_location.getText());
                prefs.close();
            } catch (URISyntaxException e) { status_area.appendText("! URI syntax incorrect !\n"); }
        } catch (IOException e) { /* do nothing */ }
    }
}