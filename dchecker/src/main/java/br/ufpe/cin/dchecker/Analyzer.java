package br.ufpe.cin.dchecker;

import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

import br.ufpe.cin.dchecker.core.DependencyChecker;
import br.ufpe.cin.dchecker.info.RunningInfo;
import br.ufpe.cin.dchecker.info.Verdict;

/**
 *
 * @author Jeanderson Candido <http://jeandersonbc.github.io>
 *
 */
public class Analyzer {

	public static void main(String[] args) throws FileNotFoundException {
		String name = args[0];
		Scanner sc = new Scanner(new BufferedInputStream(new FileInputStream(name)));

		// Parse and load all entries in memory
		Map<String, RunningInfo> all = new HashMap<>();
		while (sc.hasNext()) {
			String[] entryLineFields = sc.nextLine().split(TimestampListenerJUnit.COLUMN_SEP);

			String key = entryLineFields[0];
			RunningInfo info = new RunningInfo();
			info.setStart(Long.parseLong(entryLineFields[1]));
			info.setEnd(Long.parseLong(entryLineFields[2]));
			info.setThread(entryLineFields[3]);
			info.setHost(entryLineFields[4]);
			info.setResult(Verdict.valueOf(entryLineFields[5]));
			all.put(key, info);
		}
		sc.close();

		DependencyChecker.run(all);

	}

}
