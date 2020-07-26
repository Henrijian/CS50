#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i], name) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        int win_candidate = ranks[i];
        for (int j = i + 1; j < candidate_count; j++)
        {
            int lose_candidate = ranks[j];
            preferences[win_candidate][lose_candidate] += 1;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // TODO
    pair_count = 0;
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            int cur_prefer_count = preferences[i][j];
            int other_prefer_count = preferences[j][i];
            if (cur_prefer_count != other_prefer_count)
            {
                if (cur_prefer_count > other_prefer_count)
                {
                    pairs[pair_count].winner = i;
                    pairs[pair_count].loser = j;
                }
                else
                {
                    pairs[pair_count].winner = j;
                    pairs[pair_count].loser = i;
                }
                pair_count += 1;
            }
        }
    }
    return;
}

void merge_sort_pairs(pair unsorted_pairs[], int start, int end)
{
    if (start == end)
    {
        return;
    }
    else
    {
        int mid = round((start + end) / 2);

        // merge sort left side
        int left_count = mid - start + 1;
        pair left_pairs[left_count];
        int left_i = 0;
        for (int i = start; i <= mid; i++)
        {
            left_pairs[left_i].winner = unsorted_pairs[i].winner;
            left_pairs[left_i].loser = unsorted_pairs[i].loser;
            left_i++;
        }
        merge_sort_pairs(left_pairs, 0, left_count - 1);

        // merge sort right side
        int right_count = end - mid;
        pair right_pairs[right_count];
        int right_i = 0;
        for (int i = mid + 1; i <= end; i++)
        {
            right_pairs[right_i].winner = unsorted_pairs[i].winner;
            right_pairs[right_i].loser = unsorted_pairs[i].loser;
            right_i++;
        }
        merge_sort_pairs(right_pairs, 0, right_count - 1);

        // merge left and right side
        left_i = 0;
        right_i = 0;
        for (int i = start; i <= end; i++)
        {
            int left_strength = -1;
            if (left_i < left_count)
            {
                left_strength = preferences[left_pairs[left_i].winner][left_pairs[left_i].loser];
            }

            int right_strength = -1;
            if (right_i < right_count)
            {
                right_strength = preferences[right_pairs[right_i].winner][right_pairs[right_i].loser];
            }

            if (right_strength > left_strength)
            {
                unsorted_pairs[i].winner = right_pairs[right_i].winner;
                unsorted_pairs[i].loser = right_pairs[right_i].loser;
                right_i++;
            }
            else
            {
                unsorted_pairs[i].winner = left_pairs[left_i].winner;
                unsorted_pairs[i].loser = left_pairs[left_i].loser;
                left_i++;
            }
        }

    }
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // TODO
    merge_sort_pairs(pairs, 0, pair_count - 1);
    return;
}

bool is_graph_circle(void)
{
    bool has_source = false;
    for (int i = 0; i < candidate_count; i++)
    {
        bool link_out = false;
        bool link_in = false;
        for (int j = 0; j < candidate_count; j++)
        {
            if (j != i)
            {
                if (locked[i][j])
                {
                    link_out = true;
                }
                if (locked[j][i])
                {
                    link_in = true;
                }
            }
        }
        if (!link_in && link_out)
        {
            has_source = true;
            break;
        }
    }
    return !has_source;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // TODO
    for (int i = 0; i < pair_count; i++)
    {
        pair cur_pair = pairs[i];
        locked[cur_pair.winner][cur_pair.loser] = true;
        if (is_graph_circle())
        {
            locked[cur_pair.winner][cur_pair.loser] = false;
        }
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        bool is_source = true;
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[j][i])
            {
                is_source = false;
                break;
            }
        }
        if (is_source)
        {
            printf("%s\n", candidates[i]);
            break;
        }
    }
    return;
}

