import java.io.BufferedReader;
import java.io.FileReader;
import java.util.LinkedHashMap;
import java.util.Map;

public class FileWorker {

    public static Map<String, Float> loadTrigram() {
        FileReader fileReader;
        Map<String, Float> map = new LinkedHashMap<>();
        try {

            fileReader = new FileReader("grams/english_trigrams.txt");

            BufferedReader bufferReader = new BufferedReader(fileReader);
            String str;

            long total = 0;
            while ((str = bufferReader.readLine()) != null) {
                map.put(str.split(" ")[0], new Float(str.split(" ")[1]));
                total += Integer.parseInt(str.split(" ")[1]);
            }

            for (Map.Entry<String, Float> entry : map.entrySet()) {
                entry.setValue((float) Math.log10(entry.getValue() / total));
            }

            bufferReader.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return map;
    }
}
