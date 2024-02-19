
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # Import the 3D plotting toolkit

bone_list = [
        [
            "SPINE_CHEST",
            "SPINE_NAVEL"
        ],
        [
            "SPINE_NAVEL",
            "PELVIS"
        ],
        [
            "SPINE_CHEST",
            "NECK"
        ],
        [
            "NECK",
            "HEAD"
        ],
        [
            "HEAD",
            "NOSE"
        ],
        [
            "SPINE_CHEST",
            "CLAVICLE_LEFT"
        ],
        [
            "CLAVICLE_LEFT",
            "SHOULDER_LEFT"
        ],
        [
            "SHOULDER_LEFT",
            "ELBOW_LEFT"
        ],
        [
            "ELBOW_LEFT",
            "WRIST_LEFT"
        ],
        [
            "WRIST_LEFT",
            "HAND_LEFT"
        ],
        [
            "HAND_LEFT",
            "HANDTIP_LEFT"
        ],
        [
            "WRIST_LEFT",
            "THUMB_LEFT"
        ],
        [
            "PELVIS",
            "HIP_LEFT"
        ],
        [
            "HIP_LEFT",
            "KNEE_LEFT"
        ],
        [
            "KNEE_LEFT",
            "ANKLE_LEFT"
        ],
        [
            "ANKLE_LEFT",
            "FOOT_LEFT"
        ],
        [
            "NOSE",
            "EYE_LEFT"
        ],
        [
            "EYE_LEFT",
            "EAR_LEFT"
        ],
        [
            "SPINE_CHEST",
            "CLAVICLE_RIGHT"
        ],
        [
            "CLAVICLE_RIGHT",
            "SHOULDER_RIGHT"
        ],
        [
            "SHOULDER_RIGHT",
            "ELBOW_RIGHT"
        ],
        [
            "ELBOW_RIGHT",
            "WRIST_RIGHT"
        ],
        [
            "WRIST_RIGHT",
            "HAND_RIGHT"
        ],
        [
            "HAND_RIGHT",
            "HANDTIP_RIGHT"
        ],
        [
            "WRIST_RIGHT",
            "THUMB_RIGHT"
        ],
        [
            "PELVIS",
            "HIP_RIGHT"
        ],
        [
            "HIP_RIGHT",
            "KNEE_RIGHT"
        ],
        [
            "KNEE_RIGHT",
            "ANKLE_RIGHT"
        ],
        [
            "ANKLE_RIGHT",
            "FOOT_RIGHT"
        ],
        [
            "NOSE",
            "EYE_RIGHT"
        ],
        [
            "EYE_RIGHT",
            "EAR_RIGHT"
        ]
    ]

joint_list =  ["PELVIS", "SPINE_NAVAL", "SPINE_CHEST", "NECK", 
               "CLAVICLE_LEFT", "SHOULDER_LEFT", "ELBOW_LEFT", "WRIST_LEFT",
              "HAND_LEFT", "HANDTIP_LEFT", "THUMB_LEFT", "CLAVICLE_RIGHT", 
              "SHOULDER_RIGHT", "ELBOW_RIGHT", "WRIST_RIGHT", "HAND_RIGHT",
             "HANDTIP_RIGHT", "THUMB_RIGHT", "HIP_LEFT", "KNEE_LEFT", 
             "ANKLE_LEFT", "FOOT_LEFT", "HIP_RIGHT", "KNEE_RIGHT",
            "ANKLE_RIGHT", "FOOT_RIGHT", "HEAD", "NOSE", "EYE_LEFT",
           "EAR_LEFT", "EYE_RIGHT", "EAR_RIGHT"]

previous_bone_lengths = {}

red_bone_counter = {tuple(bone): 0 for bone in bone_list}

def draw_skeleton(ax, frame, bone_list, frame_number, previous_bone_lengths, red_bone_counter):
    ax.clear()

    # Check if 'bodies' key exists and is not empty
    if 'bodies' in frame and frame['bodies']:
        joint_positions = frame['bodies'][0]['joint_positions']
        joint_dict = {joint: position for joint, position in zip(joint_list, joint_positions)}

        for _, position in joint_dict.items():
            x, y, z = position
            ax.scatter(x, y, z, marker='o', color='blue')

        for bone in bone_list:
            if len(bone) == 2:
                start_joint, end_joint = bone
                bone_key = tuple(bone)  # Convert list to tuple

                if start_joint in joint_dict and end_joint in joint_dict:
                    start_pos = np.array(joint_dict[start_joint])
                    end_pos = np.array(joint_dict[end_joint])
                    bone_length = np.linalg.norm(end_pos - start_pos)

                    # Use bone_key to check in previous_bone_lengths
                    color = 'green'
                    if bone_key in previous_bone_lengths:
                        if abs(previous_bone_lengths[bone_key] - bone_length) > 1:
                            color = 'red'
                            red_bone_counter[bone_key] += 1

                    # Update previous_bone_lengths using bone_key
                    previous_bone_lengths[bone_key] = bone_length
                    ax.plot([start_pos[0], end_pos[0]], [start_pos[1], end_pos[1]], [start_pos[2], end_pos[2]], color=color)
    else:
        # Handle case where no bodies are detected
        print(f"No bodies detected in frame {frame_number+1}")

    # Generate and display the text for red bone counts
    red_bone_text = "Red Bone Counts:\n" + "\n".join([f"{bone}: {count}" for bone, count in red_bone_counter.items()])
    ax.text2D(0.90, 0.75, red_bone_text, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', facecolor='wheat', alpha=0.5))

    ax.set_xlim(-1000, 1000)
    ax.set_ylim(1000, -1000)
    ax.set_zlim(6000, -3000)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title(f"Frame {frame_number+1}")

# Define a function to calculate the length of a bone
def calculate_bone_length(joint_dict, bone):
    start_joint, end_joint = bone
    if start_joint in joint_dict and end_joint in joint_dict:
        start_pos = np.array(joint_dict[start_joint])
        end_pos = np.array(joint_dict[end_joint])
        length = np.linalg.norm(end_pos - start_pos)
        return length
    return 0.0  # Return 0 if one of the joints is missing

invalid = 0
# Initialize a dictionary to store lengths of each bone over time
bone_lengths_over_time = {tuple(bone): [] for bone in bone_list}

def update(num, frames, bone_list, ax, previous_bone_lengths, red_bone_counter):
    global invalid, bone_lengths_over_time
    frame = frames[num]
    draw_skeleton(ax, frame, bone_list, num, previous_bone_lengths, red_bone_counter)

    # Check if 'bodies' key exists and is not empty
    if 'bodies' in frame and frame['bodies']:
        joint_positions = frame["bodies"][0]["joint_positions"]
        joint_dict = {joint: position for joint, position in zip(joint_list, joint_positions)}
        legend_text = ""
        for bone in bone_list:
            length = calculate_bone_length(joint_dict, bone)
            bone_lengths_over_time[tuple(bone)].append(length)  # Append length
        ax.text(-2500, 0, 6000, legend_text, color='black', fontsize=10, backgroundcolor='white')
    else:
        invalid += 1
        ax.text(-2500, 0, 6000, "No bodies detected in this frame", color='black', fontsize=10, backgroundcolor='white')
        for bone in bone_list:  # Append a placeholder or NaN for frames without bodies
            bone_lengths_over_time[tuple(bone)].append(np.nan)

    # Calculate and display the percentage of missing frames
    total_frames = num + 1  # Adding 1 because frame indexing starts at 0
    missing_frame_percentage = (invalid / total_frames) * 100
    ax.text2D(0.05, 0.95, f"Missing frames: {invalid} ({missing_frame_percentage:.2f}%)", transform=ax.transAxes, color='red', fontsize=10)



def plot_bone_statistics(bone_lengths_over_time):
    # Plot for all bones
    plt.figure(figsize=(15, 10))
    for bone, lengths in bone_lengths_over_time.items():
        frames = list(range(len(lengths)))
        mean_length = np.nanmean(lengths)  # Using nanmean to ignore NaN values
        std_dev = np.nanstd(lengths)  # Using nanstd to ignore NaN values
        
        # Plot each bone's length over time
        plt.plot(frames, lengths, label=f'{bone} (Mean: {mean_length:.2f}, Std: {std_dev:.2f})')
    
    plt.title('Bone Lengths Over Time for All Bones')
    plt.xlabel('Frame')
    plt.ylabel('Length')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Specific bones groups
    bone_groups = {
        'Right Arm': [["ELBOW_RIGHT", "WRIST_RIGHT"], ["SHOULDER_RIGHT", "ELBOW_RIGHT"]],
        'Left Arm': [["ELBOW_LEFT", "WRIST_LEFT"], ["SHOULDER_LEFT", "ELBOW_LEFT"]],
        'Right Leg': [["HIP_RIGHT", "KNEE_RIGHT"], ["KNEE_RIGHT", "ANKLE_RIGHT"]],
        'Left Leg': [["HIP_LEFT", "KNEE_LEFT"], ["KNEE_LEFT", "ANKLE_LEFT"]]
    }

    # Plot for specific bone groups
    for group_name, bones in bone_groups.items():
        plt.figure(figsize=(15, 10))
        for bone in bones:
            bone = tuple(bone)  # Convert list to tuple for indexing
            if bone in bone_lengths_over_time:
                lengths = bone_lengths_over_time[bone]
                frames = list(range(len(lengths)))
                mean_length = np.nanmean(lengths)
                std_dev = np.nanstd(lengths)
                
                plt.plot(frames, lengths, label=f'{bone} (Mean: {mean_length:.2f}, Std: {std_dev:.2f})')
        
        plt.title(f'Bone Lengths Over Time for {group_name}')
        plt.xlabel('Frame')
        plt.ylabel('Length')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

def main():
    #with open("C:\\Users\\evillaro\\Downloads\\yesmarkersafter.json", "r") as file:
    with open("C:\\Users\\evillaro\\Downloads\\outputchanged.json", "r") as file:
        data = json.load(file)

    frames = data["frames"]

    fig = plt.figure(figsize=(12.8, 9.6))  # Double the default size
    ax = fig.add_subplot(111, projection='3d')  # Create a 3D subplot
    
    # Set the view angle to rotate the visualization by 45 degrees
    ax.view_init(elev=45, azim=-88)  # Adjust the values as needed
   
    ani = FuncAnimation(fig, update, frames=len(frames), fargs=(frames, bone_list, ax, previous_bone_lengths, red_bone_counter), interval=0.5)
    plt.show()
    plot_bone_statistics(bone_lengths_over_time)
    
if __name__ == "__main__":
    main()