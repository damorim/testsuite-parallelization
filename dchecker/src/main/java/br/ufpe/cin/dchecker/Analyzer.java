package br.ufpe.cin.dchecker;

import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Scanner;
import java.util.Set;

import br.ufpe.cin.dchecker.core.DependencyChecker;
import br.ufpe.cin.dchecker.model.DependencyGroup;
import br.ufpe.cin.dchecker.model.RunningInfo;
import br.ufpe.cin.dchecker.model.Verdict;

/**
 *
 * @author Jeanderson Candido <http://jeandersonbc.github.io>
 *
 */
public class Analyzer {

	public static void main(String[] args) throws FileNotFoundException {
		String path = args[0];
		Set<DependencyGroup> allDeps = DependencyChecker.dependenciesFrom(entriesFromFile(path));
		showStatisticsFrom(allDeps);
	}

	private static Map<String, RunningInfo> entriesFromFile(String path) throws FileNotFoundException {
		Scanner sc = new Scanner(new BufferedInputStream(new FileInputStream(path)));

		// Parse and load all entries in memory
		Map<String, RunningInfo> entriesFromFile = new HashMap<>();
		while (sc.hasNext()) {
			String[] entryLineFields = sc.nextLine().split(TimestampListenerJUnit.COLUMN_SEP);

			String key = entryLineFields[0];

			RunningInfo info = new RunningInfo();
			info.setStart(Long.parseLong(entryLineFields[1]));
			info.setEnd(Long.parseLong(entryLineFields[2]));
			info.setThread(entryLineFields[3]);
			info.setHost(entryLineFields[4]);
			info.setResult(Verdict.valueOf(entryLineFields[5]));

			entriesFromFile.put(key, info);
		}
		sc.close();

		return entriesFromFile;
	}

	public static void showStatisticsFrom(Set<DependencyGroup> allDeps) {
		// Statistics from allDeps
		Map<String, Integer> vms = new HashMap<>();
		int dependencyCounter = 0;
		for (DependencyGroup entry : allDeps) {
			System.out.println(entry);
			dependencyCounter += entry.size();
			RunningInfo ownerInfo = entry.getOwner().getValue();
			vms.put(ownerInfo.getHost(), !vms.containsKey(ownerInfo.getHost()) ? 1 : vms.get(ownerInfo.getHost()) + 1);
		}
		System.out.println("-------- Running Information --------");
		int vmCounter = 0;
		int total = 0;
		for (Entry<String, Integer> entry : vms.entrySet()) {
			total += entry.getValue();
			System.out.println(String.format(" %2d) %-47s %d tests", ++vmCounter, entry.getKey(), entry.getValue()));
		}
		System.out.println("-------- Statistics --------");
		System.out.println(String.format(" %12s: %d", "Total Tests", total));
		System.out.println(String.format(" %12s: %d", "Dependencies", dependencyCounter));
		System.out.println(String.format(" %12s: %d", "VM Counter", vms.size()));

	}

}
