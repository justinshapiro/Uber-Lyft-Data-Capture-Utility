package __UI__;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.ButtonType;
import javafx.scene.image.Image;
import javafx.stage.Stage;

import java.io.*;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.util.Optional;

public class UI extends Application {

    public static void main(String[] args) {
        String s = "file:///" + System.getProperty("user.dir") + "/";
        s = s.replaceAll("\\\\", "/");
        s = s.replaceAll(" ", "%20");
        try {
            try {
                URI prefs_file_location = new URI(s + "resources/preferences.txt");
                URL prefs_url = prefs_file_location.toURL();
                BufferedReader br = new BufferedReader(new InputStreamReader(prefs_url.openStream()));
                String line = br.readLine();
                br.close();
                if (line.equals("none")) {
                    PrintWriter prefs = new PrintWriter(new File(prefs_file_location), "UTF-8");
                    prefs.println("uber-lyft_result.csv");
                    prefs.println(System.getProperty("user.dir"));
                    prefs.println("locations.csv");
                    prefs.println(System.getProperty("user.dir"));
                    prefs.close();
                }
            } catch (URISyntaxException e) { System.out.println("URI syntax incorrect"); }
        } catch (IOException e) { /* do nothing */ }

        launch(args);
    }

    @Override
    public void start(Stage stage) throws Exception {
        Parent root = FXMLLoader.load(getClass().getResource("ui.fxml"));
        stage.setTitle("Uber/Lyft Data Capture Utility");
        stage.setScene(new Scene(root, 600, 450));
        stage.setResizable(false);
        stage.show();

        Platform.setImplicitExit(false);
        stage.setOnCloseRequest(event -> {
            Alert alert = new Alert(Alert.AlertType.CONFIRMATION);
            alert.setTitle("Exit Application");
            alert.setHeaderText("Data collection will terminate!");
            alert.setContentText("Choose \"OK\" to end data collection. Otherwise, choose \"Cancel\".");

            Optional<ButtonType> result = alert.showAndWait();
            if (result.isPresent() && result.get() != ButtonType.OK) {
                event.consume();
            } else {
                try {
                    Runtime.getRuntime().exec("taskkill /F /IM query_agent.exe");
                } catch (IOException e) { /* do nothing */ }
                Platform.exit();
            }
        });
    }
}
